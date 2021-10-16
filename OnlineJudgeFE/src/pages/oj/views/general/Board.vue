<template>
  <Panel shadow :padding="10">
    <div slot="title">
      {{ title }}
    </div>
    <div slot="extra">
      <Button v-if="listVisible" type="info" @click="init" :loading="btnLoading">
        {{ $t('m.Refresh') }}
      </Button>
      <Button v-else type="ghost" icon="ios-undo" @click="goBack">{{ $t('m.Back') }}</Button>
    </div>

    <transition-group name="post-animate" mode="in-out">
      <div class="no-post" v-if="!posts.length" key="no-post">
        <p>{{ $t('m.No_Announcements') }}</p>
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
      </template>
    </transition-group>
  </Panel>
</template>

<script>
import api from '@oj/api';
import Pagination from '@oj/components/Pagination';

export default {
  name: 'Board',
  components: {
    Pagination,
  },
  data() {
    return {
      limit: 10,
      total: 10,
      btnLoading: false,
      posts: [],
      post: '',
      listVisible: true,
      comments: [
        {
          'create_time': '2021-10-16 12:34',
          'created_by': 'user101',
          'content': '댓글 테스트 #1'
        },
        {
          'create_time': '2021-10-16 16:12',
          'created_by': 'user102',
          'content': '댓글 테스트 #2'
        },
        {
          'create_time': '2021-10-16 13:56',
          'created_by': 'user103',
          'content': '댓글 테스트 #3'
        }
      ]
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      if (this.isProblem) {
        this.getProblemPostList();
      } else {
        this.getPostList();
      }
    },
    getPostList(page = 1) {
      this.btnLoading = true;
      api.getPostList((page - 1) * this.limit, this.limit).then(res => {
        this.btnLoading = false;
        this.posts = res.data.data.results;
        this.total = res.data.data.total;
      }, () => {
        this.btnLoading = false;
      });
    },
    getProblemPostList() {
      this.btnLoading = true;
      api.getProblemPostList(this.$route.params.problemID).then(res => {
        this.btnLoading = false;
        this.posts = res.data.data;
      }, () => {
        this.btnLoading = false;
      });
    },
    goPost(post) {
      this.post = post;
      this.listVisible = false;
    },
    goBack() {
      this.listVisible = true;
      this.post = '';
    },
  },
  computed: {
    title() {
      if (this.listVisible) {
        return this.isProblem ? this.$i18n.t('m.Contest_Announcements') : this.$i18n.t('m.Announcements');
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
</style>
