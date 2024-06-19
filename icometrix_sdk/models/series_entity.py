from icometrix_sdk.models.base import BackendEntity, utc_datetime


class SeriesEntity(BackendEntity):
    note: str
    modality: str
    study_id: str
    echo_time: str  # available after preprocessing
    slice_gap: float  # available after preprocessing
    flip_angle: str
    image_size: list[int]  # available after preprocessing
    patient_id: str
    project_id: str
    quarantine: str
    voxel_size: list[float]  # available after preprocessing
    series_date: str
    series_time: str
    series_type: str  # available after preprocessing
    pixel_spacing: str
    sequence_name: str
    series_number: str
    inversion_time: str
    images_in_nifti: int  # available after preprocessing
    repetition_time: str
    slice_thickness: float  # available after preprocessing
    sequence_variant: str
    receive_coil_name: str
    scanning_sequence: str
    slice_orientation: str
    body_part_examined: str
    imported_timestamp: utc_datetime
    series_description: str
    transmit_coil_name: str
    series_instance_uid: str
    images_in_acquisition: str | int
    magnetic_field_strength: str
    maximum_slice_increment: float  # available after preprocessing
    expected_images_in_acquisition: str
