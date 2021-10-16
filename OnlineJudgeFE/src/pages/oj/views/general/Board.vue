<template>
<div>
  <Panel shadow :padding="10">
    <div slot="title">
      {{ title }}
    </div>
    <div slot="extra">
      <Button v-if="listVisible" type="info" @click.native="showEditPostDialog = true">
        {{ $t('m.NewPost') }}
      </Button>
      <Button v-if="listVisible" type="info" @click="init" :loading="btnLoading">
        {{ $t('m.Refresh') }}
      </Button>
      <Button v-else type="ghost" icon="ios-undo" @click="goBack">{{ $t('m.Back') }}</Button>
    </div>

    <transition-group name="post-animate" mode="in-out">
      <div class="no-post" v-if="!posts.length" key="no-post">
        <p>{{ $t('m.No_Posts') }}</p>
      </div>
      <template v-if="listVisible">
        <ul class="posts-container" key="list">
          <li v-for="post in posts" :key="post.title">
            <div class="flex-container">
              <div class="title"><a class="entry" @click="goPost(post)">
                {{ post.title }}</a></div>
              <div class="date">{{ post.create_time | localtime }}</div>
              <div class="creator"> {{ $t('m.By') }} {{ post.created_by.username }}</div>
            </div>
          </li>
        </ul>
        <Pagination v-if="!isProblem"
                    key="page"
                    :total="total"
                    :page-size="limit"
                    @on-change="getPostList">
        </Pagination>
      </template>

      <template v-else>
        <div v-katex v-html="post.content" key="content" class="content-container markdown-body"></div>
        <Card v-for="comment in comments" :key="comment.create_time">
          <a href="#" slot="title">
              {{comment.created_by}}
          </a>
          <p slot="extra">
              {{comment.create_time}}
          </p>
          <p>
            {{comment.content}}
          </p>
        </Card>
        <Card>
          <a href="#" slot="title">
              새 댓글
          </a>
          <p slot="extra">
              <Icon type="md-add" @click="writeComment(comment)"></Icon>
          </p>
          <Input v-model="comment" maxlength="500" show-word-limit type="textarea" placeholder="내용을 입력하세요..." />
        </Card>
      </template>
    </transition-group>
  </Panel>
  <el-dialog title="새 게시글" :visible.sync="showEditPostDialog"
               @open="onOpenEditDialog" :close-on-click-modal="false">
      <el-form label-position="top">
        <el-form-item :label="$t('m.Post_Title')" required>
          <el-input
            v-model="newpost.title"
            :placeholder="$t('m.Post_Title')" class="title-input">
          </el-input>
        </el-form-item>
        <el-form-item :label="$t('m.Post_Content')" required>
          <Simditor v-model="newpost.content"></Simditor>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
          <p style="color:red"> {{ this.newpostErr }} </p>
          <cancel @click.native="showEditPostDialog = false"></cancel>
          <save type="primary" @click.native="writePost"></save>
      </span>
    </el-dialog>
</div>
</template>

<script>
import api from '@oj/api';
import Pagination from '@oj/components/Pagination';
import Simditor from '@oj/components/Simditor';

export default {
  name: 'Board',
  components: {
    Pagination,
    Simditor,
  },
  data() {
    return {
      limit: 10,
      total: 10,
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
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.getPostList();
    },
    getPostList(page = 1) {
      this.btnLoading = true;
      api.getPostList((page - 1) * this.limit, this.limit, this.$route.params.problemID).then(res => {
        console.log(res);
        this.btnLoading = false;
        this.posts = res.data.data.results;
        this.total = res.data.data.total;
      }, () => {
        this.btnLoading = false;
      });
    },
    writePost() {
      if(!this.newpost.title){
        this.newpostErr = '제목은 비워둘 수 없습니다!';
        return;
      }
      if(!this.newpost.content){
        this.newpostErr = '내용은 비워둘 수 없습니다!';
        return;
      }
      api.writePost(this.newpost.title, this.newpost.content).then(res => {
        this.newpostErr = '';
        this.init();
      });
    },
    goPost(post) {
      this.post = post;
      this.listVisible = false;
      this.getComments();
    },
    goBack() {
      this.listVisible = true;
      this.post = '';
    },
    getComments(){
      api.getComments(this.post.id).then(res => {
        this.comments = res.data.data;
      });
    },
    writeComment(comment){
      api.writeComment(this.post.id, comment).then(res => {
        this.getComments();
      });
    },
    onOpenEditDialog() {
      setTimeout(() => {
        if (document.createEvent) {
          let event = document.createEvent('HTMLEvents');
          event.initEvent('resize', true, true);
          window.dispatchEvent(event);
        } else if (document.createEventObject) {
          window.fireEvent('onresize');
        }
      }, 0);
    },
  },
  computed: {
    title() {
      if (this.listVisible) {
        return this.isProblem ? this.$i18n.t('m.Problem_Posts') : this.$i18n.t('m.Posts');
      } else {
        return this.post.title;
      }
    },
    isProblem() {
      return !!this.$route.params.problemID;
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

      .creator {
        flex: none;
        width: 200px;
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
</style>
