
import jk_utils




class EnumProcessingState(jk_utils.EnumBase):

	FAILED_CRITICALLY = -2, "failed_critically"
	NOT_PROCESSED = -1, "not_processed"
	FAILED = 0, "failed"
	SUCCEEDED = 1, "succeeded"

#



