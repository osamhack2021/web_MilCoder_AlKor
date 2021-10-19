<template>
<div>
  <Panel shadow :padding="10">
    <div slot="title">
      {{ title }}
      <el-input class="problem-slot"
        placeholder="Problem ID"
        v-model="problemID"
        clearable>
      </el-input>
    </div>
    <div slot="extra">
      <ul v-if="listVisible" class="filter" >
        <li>
          <Input v-model="searchKeyword"
            @on-enter="getPostList"
            @on-click="getPostList"
            placeholder="keyword"
            icon="ios-search-strong"/>
        </li>
        <li>
          <Button type="info" icon="edit" @click.native="showEditPostDialog = true">
            {{ $t('m.NewPost') }}
          </Button>
        </li>
        <li>
          <Button type="info" @click="init" :loading="btnLoading">
            {{ $t('m.Refresh') }}
          </Button>
        </li>
      </ul>
      <template v-else>
      <Button type="ghost" icon="ios-undo" @click="goBack">{{ $t('m.Back') }}</Button>
      <Button v-if="post && user.username==post.created_by.username || isAdminRole"
        type="success" icon="edit" @click.native="showEditPostDialog = true">
        {{ $t('m.Edit') }}
      </Button>
      <Button v-if="post && user.username==post.created_by.username || isAdminRole" type="error" icon="ios-trash" @click="deletePost">
        {{ $t('m.Delete') }}
      </Button>
      </template>
    </div>

      <div class="no-post" v-if="!posts.length" key="no-post">
        <p>{{ $t('m.No_Posts') }}</p>
      </div>
      <template v-if="listVisible">
        <ul class="posts-container" key="list">
          <li v-for="post in posts" :key="post.title">
            <div class="flex-container">
              <div class="title"><a class="entry" @click="goPost(post)">
                {{ post.title }}</a></div>
              <div class="problem">
                <el-button :type="(post.problem)?'primary':'info'" size="small" round @click="$router.push('/problem/'+post.problem._id)">
                  {{problemLabel(post.problem)}}
                </el-button>
              </div>
              <div class="date">{{ post.create_time | localtime }}</div>
              <div class="creator"> {{ $t('m.By') }} {{ post.created_by.username }}</div>
            </div>
          </li>
        </ul>
        <Pagination
          key="page"
          :total="total"
          :page-size="limit"
          @on-change="getPostList">
        </Pagination>
      </template>

      <template v-if="!listVisible">
        <div v-katex v-html="post.content" key="content" class="content-container markdown-body"></div>
        <Card v-for="comment in comments" :key="comment.create_time">
          <a href="#" slot="title">
              {{comment.created_by.username}}
          </a>
          <p slot="extra">
              {{comment.create_time | localtime}}
              <Button v-if="user.username==comment.created_by.username || isAdminRole" type="error" icon="ios-trash" class="comment-btn" @click="deleteComment(comment.id)"></Button>
          </p>
          <p>
            {{comment.content}}
          </p>
        </Card>
        <Card>
          <p slot="title" class="comment-title">
            새 댓글
          </p>
          <Button type="info" slot="extra" class="comment-btn" @click="writeComment(comment)">
            <Icon type="ios-pricetag-outline"></Icon>
            작성하기
          </Button>
          <Input v-model="comment" maxlength="500" show-word-limit type="textarea" placeholder="내용을 입력하세요..." />
        </Card>
        <Pagination
          key="commentsPage"
          :total="commentsTotal"
          :page-size="commentsLimit"
          @on-change="getComments">
        </Pagination>
      </template>
  </Panel>
  <PostEditor :visible="showEditPostDialog" :postID="post.id" @closeDialog="onCloseEditDialog"></PostEditor>
</div>
</template>

<script>
import api from '@oj/api';
import Pagination from '@oj/components/Pagination';
import Simditor from '@oj/components/Simditor';
import PostEditor from '@oj/components/PostEditor';
import { mapGetters } from 'vuex';

export default {
  name: 'Board',
  components: {
    Pagination,
    Simditor,
    PostEditor,
  },
  data() {
    return {
      problemID: '',
      limit: 10,
      total: 10,
      commentsTotal: 10,
      commentsLimit: 10,
      btnLoading: false,
      posts: [],
      post: '',
      listVisible: true,
      comments: [],
      comment: '',
      showEditPostDialog: false,
      newpost: {
        title: '',
        content: '',
      },
      newpostErr: '',
      searchKeyword: '',
    };
  },
  mounted() {
    this.init();
  },
  watch: {
    $route(to, from){
      this.init();
    },
    problemID(to, from){
      if((to && to.length==4) || to=='')
        this.getPostList();
    }
  },
  methods: {
    init() {
      this.problemID = this.$route.params.problem;
      this.getPostList();
    },
    getPostList(page = 1) {
      this.btnLoading = true;
      api.getPostList((page - 1) * this.limit, this.limit, this.problemID, this.searchKeyword).then(res => {
        this.btnLoading = false;
        this.posts = res.data.data.results;
        this.total = res.data.data.total;
      }, () => {
        this.btnLoading = false;
      });
    },
    deletePost() {
      this.$confirm('정말 삭제하시겠습니까?', 'Warning', {
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        type: 'warning',
      }).then(() => {
        api.deletePost(this.post.id).then(res => {
          this.getPostList();
          this.goBack();
        });
      });
    },
    goPost(post) {
      this.listVisible = false;
      api.getPost(post.id).then(res => {
        this.post = res.data.data;
        this.getComments();
      });
    },
    goBack() {
      this.listVisible = true;
      this.post = '';
    },
    getComments(commentsPage = 1){
      api.getComments((commentsPage - 1) * this.commentsLimit, this.commentsLimit, this.post.id).then(res => {
        this.comments = res.data.data.results;
        this.commentsTotal = res.data.data.total;
      });
    },
    writeComment(comment){
      api.writeComment(this.post.id, comment).then(res => {
        this.comment = '';
        this.getComments();
      });
    },
    deleteComment(commentID) {
      this.$confirm('정말 삭제하시겠습니까?', 'Warning', {
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        type: 'warning',
      }).then(() => {
        api.deleteComment(commentID).then(res => {
          this.getComments();
        });
      });
    },
    onCloseEditDialog() {
      this.showEditPostDialog = false;
      if(this.listVisible)
        this.getPostList();
      else
       this.goPost(this.post);
    },
    problemLabel(prob){
      if(!!!prob)
        return 'General';
      return '[' + prob._id + '] ' + prob.title;
    }
  },
  computed: {
    ...mapGetters(['user', 'isAuthenticated', 'isAdminRole']),
    title() {
      if (this.listVisible) {
        return this.isProblem ? this.$i18n.t('m.Problem_Posts') : this.$i18n.t('m.Posts');
      } else {
        return this.post.title;
      }
    },
    isProblem() {
      return !!this.problemID;
    },
  },
};
</script>

<style scoped lang="less">
.posts-container {
  margin-top: -10px;
  margin-bottom: 10px;

  li {
    padding-top: 15px;
    list-style: none;
    padding-bottom: 15px;
    margin-left: 20px;
    font-size: 16px;
    border-bottom: 1px solid rgba(187, 187, 187, 0.5);

    &:last-child {
      border-bottom: none;
    }

    .flex-container {
      align-items: center;
      .title {
        flex: 1 1;
        text-align: left;
        padding-left: 10px;

        a.entry {
          color: #495060;

          &:hover {
            color: #2d8cf0;
            border-bottom: 1px solid #2d8cf0;
          }
        }
      }

      .problem {
        flex: none;
        text-align: center;
      }

      .creator {
        flex: none;
        width: 120px;
        text-align: center;
      }

      .date {
        flex: none;
        width: 200px;
        text-align: center;
      }
    }
  }
}

.flex-container {
  align-items: center;
  .flex-stretch {
    flex: 1 1;
    padding-left: 30px;
  }
  .flex-item {
    flex: none;
    padding-left: 10px;
  }
}

.problem-slot {
  max-width: 120px;
}

.content-container {
  padding: 0 20px 20px 20px;
}

.no-post {
  text-align: center;
  font-size: 16px;
}

changeLocale
.post-animate-enter-active {
  animation: fadeIn 1s;
}

.title-input {
  margin-bottom: 20px;
}

.comment-title {
  margin-bottom: 0;
}

.comment-btn {
  margin-top: -5px;
}
</style>
