import moment from 'moment';
import time from './time';
import utils from './utils';

function fromNow(time) {
  return moment(time * 3).fromNow();
}

export default {
  submissionMemory: utils.submissionMemoryFormat,
  submissionTime: utils.submissionTimeFormat,
  localtime: time.utcToLocal,
  fromNow: fromNow,
};
