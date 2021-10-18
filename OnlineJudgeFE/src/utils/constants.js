export const COMPILE_ERROR = -2;
export const WRONG_ANSWER = -1;
export const ACCEPTED = 0;
export const TIME_LIMIT_EXCEEDED = 1;
export const TIME_LIMIT_EXCEEDED_2 = 2;
export const MEMORY_LIMIT_EXCEEDED = 3;
export const RUNTIME_ERROR = 4;
export const SYSTEM_ERROR = 5;
export const PENDING = 6;
export const JUDGING = 7;
export const PARTIAL_ACCEPTED = 8;
export const SUBMITTING = 9;

export const JUDGE_STATUS = {
  [COMPILE_ERROR]: {
    name: 'Compile Error',
    short: 'CE',
    color: 'yellow',
    type: 'warning',
  },
  [WRONG_ANSWER]: {
    name: 'Wrong Answer',
    short: 'WA',
    color: 'red',
    type: 'error',
  },
  [ACCEPTED]: {
    name: 'Accepted',
    short: 'AC',
    color: 'green',
    type: 'success',
  },
  [TIME_LIMIT_EXCEEDED]: {
    name: 'Time Limit Exceeded',
    short: 'TLE',
    color: 'red',
    type: 'error',
  },
  [TIME_LIMIT_EXCEEDED_2]: {
    name: 'Time Limit Exceeded',
    short: 'TLE',
    color: 'red',
    type: 'error',
  },
  [MEMORY_LIMIT_EXCEEDED]: {
    name: 'Memory Limit Exceeded',
    short: 'MLE',
    color: 'red',
    type: 'error',
  },
  [RUNTIME_ERROR]: {
    name: 'Runtime Error',
    short: 'RE',
    color: 'red',
    type: 'error',
  },
  [SYSTEM_ERROR]: {
    name: 'System Error',
    short: 'SE',
    color: 'red',
    type: 'error',
  },
  [PENDING]: {
    name: 'Pending',
    color: 'yellow',
    type: 'warning',
  },
  [JUDGING]: {
    name: 'Judging',
    color: 'blue',
    type: 'info',
  },
  [PARTIAL_ACCEPTED]: {
    name: 'Partial Accepted',
    short: 'PAC',
    color: 'blue',
    type: 'info',
  },
  [SUBMITTING]: {
    name: 'Submitting',
    color: 'yellow',
    type: 'warning',
  },
};

export const CONTEST_STATUS = {
  'NOT_START': '1',
  'UNDERWAY': '0',
  'ENDED': '-1',
};

export const CONTEST_STATUS_REVERSE = {
  '1': {
    name: 'Not Started',
    color: 'yellow',
  },
  '0': {
    name: 'Underway',
    color: 'green',
  },
  '-1': {
    name: 'Ended',
    color: 'red',
  },
};

export const RULE_TYPE = {
  ACM: 'ACM',
  OI: 'OI',
};

export const CONTEST_TYPE = {
  PUBLIC: 'Public',
  PRIVATE: 'Password Protected',
};

export const USER_TYPE = {
  REGULAR_USER: 'Regular User',
  ADMIN: 'Admin',
  SUPER_ADMIN: 'Super Admin',
};

export const PROBLEM_PERMISSION = {
  NONE: 'None',
  OWN: 'Own',
  ALL: 'All',
};

export const STORAGE_KEY = {
  AUTHED: 'authed',
  PROBLEM_CODE: 'problemCode',
  languages: 'languages',
};

export function buildProblemCodeKey(problemID, contestID = null) {
  if (contestID) {
    return `${STORAGE_KEY.PROBLEM_CODE}_${contestID}_${problemID}`;
  }
  return `${STORAGE_KEY.PROBLEM_CODE}_NaN_${problemID}`;
}

export const GOOGLE_ANALYTICS_ID = 'UA-111499601-1';
