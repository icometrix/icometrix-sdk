import logging

from pydicom import Dataset, DataElement

from icometrix_sdk.anonymizer.exceptions import PolicyException
from icometrix_sdk.anonymizer.hash_factory import HashMethod
from icometrix_sdk.anonymizer.models import Policy, TagPolicy
from icometrix_sdk.anonymizer.utils import remove_tag, replace_tag, hash_tag, _is_pixel_data, round_tag, \
    add_de_identification_tags, is_tag, is_group, empty_tag

logger = logging.getLogger(__name__)


class Anonymizer:
    default_policy: TagPolicy = TagPolicy("empty", "Default")

    def __init__(self, policy: Policy, group_policy: Policy, hash_algo: HashMethod):
        for tag in policy:
            if not is_tag(tag):
                raise PolicyException("Tag policy contains an invalid tag")

        for group in group_policy:
            if not is_group(group):
                raise PolicyException("Group policy contains an invalid group")

        self.policy = policy
        self.group_policy = group_policy
        self.hash_algo = hash_algo

    def anonymize(self, dataset: Dataset) -> Dataset:
        for element in dataset.iterall():
            # Keep the pixel data
            if _is_pixel_data(element.tag):
                continue

            # Apply the tag policy
            elif element.tag in self.policy:
                tag_policy = self.policy[element.tag]
                self._apply_policy_to_tag(element, tag_policy, dataset)

            # Apply the group policy
            elif element.tag.group in self.group_policy:
                tag_policy = self.group_policy[element.tag.group]
                self._apply_policy_to_group(element, tag_policy, dataset)

            # Apply the default policy
            else:
                self._apply_policy_to_tag(element, self.default_policy, dataset)

        return add_de_identification_tags(dataset)

    def _apply_policy_to_group(self, element: DataElement, tag_policy: TagPolicy, dataset: Dataset):
        try:
            self._apply_policy_to_tag(element, tag_policy, dataset)
        except (AttributeError, ValueError):
            logger.debug("Failed to apply group action '%d' to %s %s.", tag_policy.action,
                         element.tag, element.name)
            return

    def _apply_policy_to_tag(self, element: DataElement, tag_policy: TagPolicy, dataset: Dataset):
        logger.debug('%d %s: %s', element.tag, element.name, tag_policy.action)

        if tag_policy.action == "keep":
            return
        elif tag_policy.action == "empty":
            empty_tag(element)
        elif tag_policy.action == "remove":
            remove_tag(element, dataset)
        elif tag_policy.action == "replace":
            replace_tag(element, dataset, tag_policy.replace_fn)
        elif tag_policy.action == "hash":
            hash_tag(element, self.hash_algo)
        elif tag_policy.action == "round":
            round_tag(element)
        else:
            raise ValueError("Unknown tag policy action")
