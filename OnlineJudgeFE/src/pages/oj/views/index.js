import NotFound from './general/404.vue';
import Announcements from './general/Announcements.vue';
import Home from './general/Home.vue';
import About from './help/About.vue';
import FAQ from './help/FAQ.vue';
import ProblemList from './problem/ProblemList.vue';
import Logout from './user/Logout.vue';
import UserHome from './user/UserHome.vue';

// Grouping Components in the Same Chunk
const SubmissionList = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionList.vue');
const SubmissionDetails = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionDetails.vue');

const ACMRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/ACMRank.vue');
const OIRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/OIRank.vue');

const ApplyResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ApplyResetPassword.vue');
const ResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ResetPassword.vue');

const Problem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/Problem.vue');

export {
  Home, NotFound, Announcements,
  Logout, UserHome, About, FAQ,
  ProblemList, Problem,
  ACMRank, OIRank,
  SubmissionList, SubmissionDetails,
  ApplyResetPassword, ResetPassword,
};
/* Component export is divided into two categories,
 * one is commonly used for direct export,
 * the other is lazy loading, such as Login, Logout, etc., lazy loading is not exported here
 *   Load in the corresponding route
 *   See https://router.vuejs.org/en/advanced/lazy-loading.html
 */
