import pydicom
from datetime import date, timedelta
from typing import Final, List, Tuple, Union

from icometrix_sdk.utils.hash_factory import HashMethod


class Anonymizer:
    """
    The anonymizer anonymizes DICOMs by:
    (1) replacing certain fields with a hash of the fields (such as UIDs)
    (2) shifting dates so that the birthday is alwasy set to the 1st of january of the birth year
    (3) removing all fields that are not anonymized or explicitly marked as to be kept.
    """

    # CONSTS
    BIRTHDAY_TAG: int = 0x00100030
    AGE_TAG: int = 0x00101010
    PATIENT_IDENTITY_REMOVED_TAG: int = 0x00120062
    DEIDENTIFICATION_METHOD_TAG: int = 0x00120063

    '''
    DICOM makes extensive use of Unique Identifiers. Almost every entity in the DICOM Data Model 
    has a unique identifier. In DICOM every SOP Class have its UID. All pre-defined UID's including 
    the SOP Class UID's are documented in chapter 6 of the DICOM standard. A DICOM Object is an 
    Instance of such class and is called SOP Instance and it also has a UID called SOP Instance UID.
    DICOM defines a mechanism in order to make sure UID's are globally Unique:

    Every DICOM application should acquire a "root" UID that is used as a prefix to the UID's it 
    creates.

    See https://dicomiseasy.blogspot.com/2011/12/chapter-4-dicom-objects-in-chapter-3.html
    '''
    ROOT_UID: Final[str] = "1.2.826.0.1.3680043.9.5542"

    def __init__(self, hash_method: HashMethod, override_whitelist_tags: List[int] = None,
                 override_whitelist_groups: List[int] = None,
                 override_whitelist_ranges: List[Tuple[int, int]] = None):

        self.hash_method = hash_method

        # Maximum age of a patient, because our population database only goes up to 90
        self.maximum_age = 90

        self.hash_uid_tags = [
            0x0020000d,  # StudyInstanceUID
            0x00200052,  # FrameOfReferenceUID
            0x00200200,  # SynchronizationFrameOfReferenceUID
            0x00080018,  # SOPInstanceUID
            0x00080014,  # InstanceCreatorUID
            0x00081155,  # RefSOPInstanceUID
            0x0020000e,  # SeriesInstanceUID
            0x0040a124,  # UID
            0x0070031a,  # FiducialUID
            0x00880140,  # StorageMediaFilesetUID
            0x30060024,  # ReferencedFrameOfReferenceUID
            0x300600c2,  # RelatedFrameOfReferenceUID
            0x300a0013  # DoseReferenceUID
        ]

        self.hash_name_tags = [
            0x00100010,  # PatientName
            0x00080090  # ReferringPhysicianName
        ]

        self.hash_tags = [
            0x00080050,  # AccessionNumber
            0x00080080,  # InstitutionName
            0x00100020,  # PatientId
            0x00100021,  # IssuerOfPatientID
            0x00101000,  # OtherPatientIDs
            0x00200010  # StudyID
        ]

        self.date_tags = [
            0x00080013,  # InstanceCreationDate
            0x00080020,  # StudyDate
            0x00080021,  # SeriesDate
            0x00080022,  # AcquisitionDate
            0x00080023,  # ContentDate
        ]

        self.time_tags = [
            0x00080013,  # InstanceCreationTime
            0x00080030,  # StudyTime
            0x00080031,  # SeriesTime
            0x00080032,  # AcquisitionTime,
            0x00180080,  # RepetitionTime
            0x00180081,  # EchoTime
            0x00180082  # InversionTime
        ]

        self.additional_whitelist_tag = [
            self.BIRTHDAY_TAG,
            0x00100040,  # PatientsSex
            0x00020000,  # MetaElementGroupLength
            0x00020001,  # FileMetaInfoVersion
            0x00020002,  # MediaStorageSOPClassUID
            0x00020003,  # MediaStorageSOPInstanceUID
            0x00020010,  # TransferSyntaxUID
            0x00020012,  # ImplementationClassUID
            # 0x00097772,  # CallingAET
        ] if override_whitelist_tags is None else override_whitelist_tags

        self.whitelisted_groups = [
            0x0008,  # Identifying information
            0x0015,  # icometrix private tags
            0x0018,  # Acquisition: mage acquisition device and imaging procedure
            0x0020,  # Relationship: Info relating the image to the location within the patient
            0x0028,  # Image presentation: manner in which the image can be presented or displayed
            0x0029,  # Groups specific to diffusion (b-vector and b-value, ...) Requested by Thibo
            0x5200,  # Multi-frame Functional Groups
        ] if override_whitelist_groups is None else override_whitelist_groups

        self.whitelisted_group_ranges = [
            (0x7f00, 0x7fff),  # Image pixel data
            (0xfff0, 0xffff)  # Needed to check after every SQ
        ] if override_whitelist_ranges is None else override_whitelist_ranges

    def anonymize(self, dicom: pydicom.FileDataset) -> pydicom.FileDataset:
        """
        Anonymizes a single FileDataSet by only keeping whitelisted tags, and hashing the necessary
        ones.

        :param dicom: dicom (pydicom.FileDataset): DICOM FileDataSet to be anonymized
        :return:  pydicom.FileDataset: Anonymized FileDataSet
        """

        anonymized_dicom = dicom.copy()

        time_shift = self._calculate_time_shift(dicom)

        for data_element in anonymized_dicom:

            tag = data_element.tag
            tag_value = data_element.value

            if tag_value is None:
                continue

            if not self._is_tag_whitelisted(tag):
                # Unsigned Short or Unsigned Long => should be numeric value
                if data_element.VR in ("US", "UL"):
                    anonymized_dicom[tag] = self._build_dataelem(data_element, 0)
                else:
                    anonymized_dicom[tag] = self._build_dataelem(data_element, "")
            elif tag in self.hash_uid_tags:
                anonymized_dicom[tag] = self._build_dataelem(
                    data_element, self.hash_uid(str(tag_value)))
            elif tag in self.hash_tags:
                anonymized_dicom[tag] = self._hash_dataelement(data_element)
            elif tag in self.hash_name_tags:
                anonymized_dicom[tag] = self._hash_dataelement(data_element)
            elif tag in self.time_tags:
                anonymized_dicom[tag] = self._build_dataelem(data_element, "010101")
            elif tag in self.date_tags:
                date_str = str(tag_value)
                orig_date = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:8]))
                shifted_date = orig_date - time_shift
                anonymized_dicom[tag] = self._build_dataelem(
                    data_element,
                    f"{shifted_date.year}{shifted_date.month:02d}{shifted_date.day:02d}")

        # Field "PatientIdentityRemoved"
        # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120062
        anonymized_dicom.add_new(self.PATIENT_IDENTITY_REMOVED_TAG, "LT", "YES")

        # Field "Deidentification method"
        # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120063
        anonymized_dicom.add_new(self.DEIDENTIFICATION_METHOD_TAG, "LT",
                                 "Python based, HIPAA compliant, based on DICOM PS3.15 AnnexE.")

        return anonymized_dicom

    def _hash(self, obj: str, max_len=0) -> str:
        output = self.hash_method.calculate_hash(obj)

        if max_len and len(output) > max_len:
            output = output[:max_len]

        return output

    def hash_id(self, id_str: str, max_len=64):
        """

        :param id_str: id that needs to be hashed
        :param max_len: max length of the hash, i.e. 64 characters for LONG STRING
        :return: dicom-compliant hashed id, i.e., the hash of the ID with an even length
        """
        hashed_id = self._hash(id_str, max_len=max_len)

        # If value length is uneven, make it even
        if len(hashed_id) % 2 != 0:
            hashed_id = hashed_id[:-1]

        return hashed_id

    def hash_uid(self, uid: str, max_len=64, trim=False) -> str:

        # In icobridge code, sometimes only the last part of the uid is hashed
        # So this is an option here for backwards compatability
        to_hash = uid.split('.')[-1] if trim else uid

        output = self._hash(to_hash)

        # Convert hash in hexadecimal format to decimal format
        # Requirement of DICOM UIDs that they only exist of digits
        # See https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_9.html
        output = str(int(output, base=16))

        # Dicom 9.1: The first digit of each component shall not be zero,
        # unless the component is a single digit.
        # See https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_9.html
        extra = ""
        if output[0] == "0":
            extra = "9"

        output = f"{self.ROOT_UID}.{extra}{output}"

        # DICOM 9.1: UIDs, shall not exceed 64 total characters
        if len(output) > max_len:
            output = output[:max_len]

        return output

    def _hash_dataelement(self, data_elem: pydicom.DataElement) -> pydicom.DataElement:
        max_len = 0
        # Short string has a max length of 16
        if data_elem.VR == "SH":
            max_len = 16
        value_hash = self._hash(data_elem.value, max_len=max_len)
        return pydicom.DataElement(VR=data_elem.VR, tag=data_elem.tag, value=value_hash)

    def _is_tag_whitelisted(self, tag) -> bool:

        # Concatenated version of all tags: combine lists and flatten them
        whitelisted_tags = [tag for sublist in
                            [self.hash_uid_tags, self.hash_name_tags, self.hash_tags,
                             self.time_tags, self.date_tags, self.additional_whitelist_tag]
                            for tag in sublist]

        if tag in whitelisted_tags:
            return True

        for group in self.whitelisted_groups:
            lower_bound = group * 0x10000
            upper_bound = group * 0x10000 + 0xffff
            if lower_bound <= tag <= upper_bound:
                return True

        for group_range in self.whitelisted_group_ranges:
            lower_range_bound = group_range[0]
            upper_range_bound = group_range[1]
            lower_bound = lower_range_bound * 0x10000
            upper_bound = upper_range_bound * 0x10000 + 0xffff

            if lower_bound <= tag <= upper_bound:
                return True

        return False

    @staticmethod
    def _build_dataelem(data_elem: pydicom.DataElement, value: Union[str, int]) \
            -> pydicom.DataElement:
        return pydicom.DataElement(VR=data_elem.VR, value=value, tag=data_elem.tag)

    def _calculate_time_shift(self, dicom: pydicom.FileDataset) -> timedelta:
        """
        Return the appropriate time shift. This is defined as the difference between
        the birthdate of the patient and the first of january. If no birthdate is given,
        and instead an age is given, the time shift is 0.
        """

        birthday_dataelem = dicom[self.BIRTHDAY_TAG]

        # Calculate anchor date: the date on which the time shift is based
        # First, check if we have the necessary data
        if birthday_dataelem is None:
            return timedelta(days=0)

        birthday = birthday_dataelem.value
        if not isinstance(birthday, str):
            return timedelta(days=0)

        # Birthday is set, so we take (month, day) to calculate the time shift
        if len(birthday) != 8:
            return timedelta(days=0)
        anchor_date = date(int(birthday[:4]), int(birthday[4:6]), int(birthday[6:8]))

        january_1 = date(anchor_date.year, 1, 1)
        return anchor_date - january_1
