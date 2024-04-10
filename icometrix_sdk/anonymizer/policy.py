from icometrix_sdk.anonymizer.models import TagPolicy, Policy

policy: Policy = {
    0x0020000d: TagPolicy("hash", "StudyInstanceUID"),
    0x00200052: TagPolicy("hash", "FrameOfReferenceUID"),
    0x00200200: TagPolicy("hash", "SynchronizationFrameOfReferenceUID"),
    0x00080018: TagPolicy("hash", "SOPInstanceUID"),
    0x00080014: TagPolicy("hash", "InstanceCreatorUID"),
    0x00081155: TagPolicy("hash", "RefSOPInstanceUID"),
    0x0020000e: TagPolicy("hash", "SeriesInstanceUID"),
    0x0040a124: TagPolicy("hash", "UID"),
    0x0070031a: TagPolicy("hash", "FiducialUID"),
    0x00880140: TagPolicy("hash", "StorageMediaFilesetUID"),
    0x30060024: TagPolicy("hash", "ReferencedFrameOfReferenceUID"),
    0x300600c2: TagPolicy("hash", "RelatedFrameOfReferenceUID"),
    0x300a0013: TagPolicy("hash", "DoseReferenceUID"),

    0x00100010: TagPolicy("hash", "PatientName"),
    # 0x00100010: TagPolicy("replace", "PatientName", "test"),
    0x00080090: TagPolicy("keep", "ReferringPhysicianName"),

    0x00080050: TagPolicy("keep", "AccessionNumber"),
    0x00080080: TagPolicy("keep", "InstitutionName"),
    0x00100020: TagPolicy("hash", "PatientId"),
    0x00100021: TagPolicy("hash", "IssuerOfPatientID"),
    0x00101000: TagPolicy("hash", "OtherPatientIDs"),
    0x00200010: TagPolicy("hash", "StudyID"),

    0x00080020: TagPolicy("keep", "StudyDate"),
    0x00080021: TagPolicy("keep", "SeriesDate"),
    0x00080022: TagPolicy("keep", "AcquisitionDate"),
    0x00080023: TagPolicy("keep", "ContentDate"),

    0x00080013: TagPolicy("keep", "ContentDate"),
    0x00080030: TagPolicy("keep", "StudyTime"),
    0x00080031: TagPolicy("keep", "SeriesTime"),
    0x00080032: TagPolicy("keep", "AcquisitionTime"),
    0x00180080: TagPolicy("keep", "RepetitionTime"),
    0x00180081: TagPolicy("keep", "EchoTime"),
    0x00180082: TagPolicy("keep", "InversionTime"),

    0x00100030: TagPolicy("round", "Patient Birthday"),
    0x00100040: TagPolicy("keep", "PatientsSex"),
    0x00020000: TagPolicy("keep", "MetaElementGroupLength"),
    0x00020001: TagPolicy("keep", "FileMetaInfoVersion"),
    0x00020002: TagPolicy("keep", "MediaStorageSOPClassUID"),
    0x00020003: TagPolicy("keep", "MediaStorageSOPInstanceUID"),
    0x00020010: TagPolicy("keep", "TransferSyntaxUID"),
    0x00020012: TagPolicy("keep", "ImplementationClassUID"),
    0x00097772: TagPolicy("keep", "CallingAET"),
}

group_policy: Policy = {
    0x0008: TagPolicy("keep", "StudyInstanceUID"),
    0x0018: TagPolicy("keep", "Acquisition: mage acquisition device and imaging procedure"),
    0x0020: TagPolicy("keep", "Relationship: Info relating the image to the location within the patient"),
    0x0028: TagPolicy("keep", "Image presentation: manner in which the image can be presented or displayed"),
    0x0029: TagPolicy("keep", "Groups specific to diffusion (b-vector and b-value, ...)"),
    0x5200: TagPolicy("keep", "Multi-frame Functional Groups"),
}
