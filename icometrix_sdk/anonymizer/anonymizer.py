from pydicom import Dataset, DataElement

from icometrix_sdk.anonymizer.hash_factory import HashMethod
from icometrix_sdk.anonymizer.models import Policy, TagPolicy
from icometrix_sdk.anonymizer.utils import remove_tag, replace_tag, hash_tag, _is_pixel_data, round_tag, \
    add_de_identification_tags


class Anonymizer:
    default_policy: TagPolicy = TagPolicy("remove", "Default")

    def __init__(self, policy: Policy, group_policy: Policy, hash_algo: HashMethod):
        self.policy = policy
        self.group_policy = group_policy
        self.hash_algo = hash_algo

    def anonymize(self, dataset: Dataset) -> Dataset:
        for element in dataset:
            # Keep the pixel data
            if _is_pixel_data(element.tag):
                continue

            # Apply the tag policy
            elif element.tag in self.policy:
                tag_policy = self.policy[element.tag]
                self._apply_policy_to_tag(element, tag_policy)

            # Apply the group policy
            elif element.tag.group in self.group_policy:
                tag_policy = self.group_policy[element.tag.group]
                self._apply_policy_to_tag(element, tag_policy)

            # Apply the default policy
            else:
                self._apply_policy_to_tag(element, self.default_policy)

        return add_de_identification_tags(dataset)

    def _apply_policy_to_tag(self, element: DataElement, tag_policy: TagPolicy):
        if tag_policy.action == "keep":
            return
        elif tag_policy.action == "remove":
            remove_tag(element)
        elif tag_policy.action == "replace":
            replace_tag(element, tag_policy.value)
        elif tag_policy.action == "hash":
            hash_tag(element, self.hash_algo)
        elif tag_policy.action == "round":
            round_tag(element)
