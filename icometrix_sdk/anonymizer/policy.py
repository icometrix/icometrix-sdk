from icometrix_sdk.anonymizer.models import TagPolicy, Policy
from icometrix_sdk.anonymizer.utils import short_md5_hash, remove_if_birthday, short_sha3_hash

group_policy: Policy = {
    0x0008: TagPolicy("keep", "Group 8"),
    0x0018: TagPolicy("keep", "Acquisition: mage acquisition device and imaging procedure"),
    0x0020: TagPolicy("keep", "Relationship: Info relating the image to the location within the patient"),
    0x0028: TagPolicy("keep", "Image presentation: manner in which the image can be presented or displayed"),
    0x0029: TagPolicy("keep", "Groups specific to diffusion (b-vector and b-value, ...)"),
    0x0040: TagPolicy("remove", "Group 40"),
    0x0051: TagPolicy("keep", "DICOM HDR"),
    0x5200: TagPolicy("keep", "Multi-frame Functional Groups"),
}

policy_sha: Policy = {
    # GROUP 0x0002
    0x00020000: TagPolicy("keep", "MetaElementGroupLength"),
    0x00020001: TagPolicy("keep", "FileMetaInfoVersion"),
    0x00020002: TagPolicy("keep", "MediaStorageSOPClassUID"),
    0x00020003: TagPolicy("keep", "MediaStorageSOPInstanceUID"),
    0x00020010: TagPolicy("keep", "TransferSyntaxUID"),
    0x00020012: TagPolicy("keep", "ImplementationClassUID"),

    # GROUP 0x0008
    0x00080013: TagPolicy("round", "InstanceCreationTime"),
    0x00080014: TagPolicy("hash", "InstanceCreatorUID"),
    0x00080018: TagPolicy("hash", "SOPInstanceUID"),
    0x00080030: TagPolicy("round", "StudyTime"),
    0x00080031: TagPolicy("round", "SeriesTime"),
    0x00080032: TagPolicy("round", "AcquisitionTime"),
    0x00080033: TagPolicy("round", "ContentTime"),
    0x00080081: TagPolicy("remove", "InstitutionAddress"),
    0x00081010: TagPolicy("remove", "StationName"),
    0x00081040: TagPolicy("remove", "InstitutionalDepartmentName"),
    0x00081060: TagPolicy("remove", "NameofPhysician(s)ReadingStudy"),
    0x00081070: TagPolicy("remove", "OperatorsName"),
    0x00081155: TagPolicy("hash", "RefSOPInstanceUID"),
    0x00082111: TagPolicy("remove", "DerivationDescription"),

    # GROUP 0x0009
    0x00097772: TagPolicy("keep", "CallingAET"),

    # GROUP 0x0010
    0x00100010: TagPolicy("replace", "PatientName", replace_fn=short_sha3_hash),
    0x00100020: TagPolicy("replace", "PatientID", replace_fn=short_sha3_hash),
    0x00100021: TagPolicy("replace", "IssuerOfPatientID", replace_fn=short_sha3_hash),
    0x00100030: TagPolicy("round", "PatientBirthday"),
    0x00100032: TagPolicy("remove", "PatientBirthTime"),
    0x00100040: TagPolicy("keep", "PatientsSex"),
    0x00101000: TagPolicy("replace", "OtherPatientIDs", replace_fn=short_sha3_hash),
    0x00101010: TagPolicy("replace", "PatientAge", replace_fn=remove_if_birthday),
    0x00101030: TagPolicy("remove", "PatientWeight"),
    0x00101040: TagPolicy("remove", "PatientAddress"),

    # GROUP 0x0020
    0x00200010: TagPolicy("replace", "StudyID", replace_fn=short_sha3_hash),
    0x0020000d: TagPolicy("hash", "StudyInstanceUID"),
    0x00200052: TagPolicy("hash", "FrameOfReferenceUID"),
    0x00200200: TagPolicy("hash", "SynchronizationFrameOfReferenceUID"),
    0x0020000e: TagPolicy("hash", "SeriesInstanceUID"),
    0x00204000: TagPolicy("remove", "ImageComments"),

    # GROUP 0x0032
    0x00321060: TagPolicy("remove", "RequestedProcedureDescription"),
    0x00324000: TagPolicy("remove", "StudyComments"),

    # GROUP 0x0040
    0x0040a124: TagPolicy("hash", "UID"),

    # GROUP 0x0070
    0x0070031a: TagPolicy("hash", "FiducialUID"),

    # GROUP 0x0088
    0x00880140: TagPolicy("hash", "StorageMediaFilesetUID"),

    # GROUP 0x3006
    0x30060024: TagPolicy("hash", "ReferencedFrameOfReferenceUID"),
    0x300600c2: TagPolicy("hash", "RelatedFrameOfReferenceUID"),
    0x300a0013: TagPolicy("hash", "DoseReferenceUID"),
}

policy_md5: Policy = {
    # GROUP 0x0002
    0x00020000: TagPolicy("keep", "MetaElementGroupLength"),
    0x00020001: TagPolicy("keep", "FileMetaInfoVersion"),
    0x00020002: TagPolicy("keep", "MediaStorageSOPClassUID"),
    0x00020003: TagPolicy("keep", "MediaStorageSOPInstanceUID"),
    0x00020010: TagPolicy("keep", "TransferSyntaxUID"),
    0x00020012: TagPolicy("keep", "ImplementationClassUID"),

    # GROUP 0x0008
    0x00080013: TagPolicy("round", "InstanceCreationTime"),
    0x00080014: TagPolicy("hash", "InstanceCreatorUID"),
    0x00080018: TagPolicy("hash", "SOPInstanceUID"),
    0x00080030: TagPolicy("round", "StudyTime"),
    0x00080031: TagPolicy("round", "SeriesTime"),
    0x00080032: TagPolicy("round", "AcquisitionTime"),
    0x00080033: TagPolicy("round", "ContentTime"),
    0x00080081: TagPolicy("remove", "InstitutionAddress"),
    0x00081010: TagPolicy("remove", "StationName"),
    0x00081040: TagPolicy("remove", "InstitutionalDepartmentName"),
    0x00081060: TagPolicy("remove", "NameofPhysician(s)ReadingStudy"),
    0x00081070: TagPolicy("remove", "OperatorsName"),
    0x00081155: TagPolicy("hash", "RefSOPInstanceUID"),
    0x00082111: TagPolicy("remove", "DerivationDescription"),

    # GROUP 0x0009
    0x00097772: TagPolicy("keep", "CallingAET"),

    # GROUP 0x0010
    0x00100010: TagPolicy("replace", "PatientName", replace_fn=short_md5_hash),
    0x00100020: TagPolicy("replace", "PatientID", replace_fn=short_md5_hash),
    0x00100021: TagPolicy("replace", "IssuerOfPatientID", replace_fn=short_md5_hash),
    0x00100030: TagPolicy("round", "PatientBirthday"),
    0x00100032: TagPolicy("remove", "PatientBirthTime"),
    0x00100040: TagPolicy("keep", "PatientsSex"),
    0x00101000: TagPolicy("replace", "OtherPatientIDs", replace_fn=short_md5_hash),
    0x00101010: TagPolicy("replace", "PatientAge", replace_fn=remove_if_birthday),
    0x00101030: TagPolicy("remove", "PatientWeight"),
    0x00101040: TagPolicy("remove", "PatientAddress"),

    # GROUP 0x0020
    0x00200010: TagPolicy("replace", "StudyID", replace_fn=short_md5_hash),
    0x0020000d: TagPolicy("hash", "StudyInstanceUID"),
    0x00200052: TagPolicy("hash", "FrameOfReferenceUID"),
    0x00200200: TagPolicy("hash", "SynchronizationFrameOfReferenceUID"),
    0x0020000e: TagPolicy("hash", "SeriesInstanceUID"),
    0x00204000: TagPolicy("remove", "ImageComments"),

    # GROUP 0x0032
    0x00321060: TagPolicy("remove", "RequestedProcedureDescription"),
    0x00324000: TagPolicy("remove", "StudyComments"),

    # GROUP 0x0040
    0x0040a124: TagPolicy("hash", "UID"),

    # GROUP 0x0070
    0x0070031a: TagPolicy("hash", "FiducialUID"),

    # GROUP 0x0088
    0x00880140: TagPolicy("hash", "StorageMediaFilesetUID"),

    # GROUP 0x3006
    0x30060024: TagPolicy("hash", "ReferencedFrameOfReferenceUID"),
    0x300600c2: TagPolicy("hash", "RelatedFrameOfReferenceUID"),
    0x300a0013: TagPolicy("hash", "DoseReferenceUID"),
}
