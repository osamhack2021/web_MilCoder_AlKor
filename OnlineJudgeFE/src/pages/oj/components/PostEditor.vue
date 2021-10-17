<template>
  <el-dialog :title="modeTitle" :visible.sync="_visible" :close-on-click-modal="false"
            @open="onOpenEditDialog" @close="onCloseEditDialog">
    <el-form label-position="top">
    <el-form-item :label="$t('m.Post_Title')" required>
        <el-input
        v-model="title"
        :placeholder="$t('m.Post_Title')" class="title-input">
        </el-input>
    </el-form-item>
    <el-form-item :label="$t('m.Post_Content')" required>
        <Simditor v-model="content"></Simditor>
    </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
        <p style="color:red"> {{ this.errMsg }} </p>
        <cancel @click.native="onCloseEditDialog"></cancel>
        <save type="primary" @click.native="writePost"></save>
    </span>
</el-dialog>
</template>

<script>
import api from '@oj/api';
import Simditor from '@oj/components/Simditor';

export default {
  name: 'PostEditor',
  components: {
    Simditor,
  },
  props: ['postID', 'visible'],
  data() {
    return {
      title: '',
      content: '',
      errMsg: '',
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
        if(this.postID){
            api.getPost(this.postID).then(res => {
                this.title = res.data.data.title;
                this.content = res.data.data.content;
            });
        }
        else{
            this.title = '';
            this.content = '';
            this.errMsg = '';
        }
    },
    writePost() {
      if(!this.title){
        this.errMsg = '제목은 비워둘 수 없습니다!';
        return;
      }
      if(!this.content){
        this.errMsg = '내용은 비워둘 수 없습니다!';
        return;
      }
      if(this.mode=='writePost'){
        api.writePost(this.title, this.content).then(res => {
          this.visible = false;
          this.init();
        });
      }
      else{
        api.editPost(this.postID, this.title, this.content).then(res => {
          this.visible = false;
          this.init();
        });
      }
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
      this.init();
    },
    onCloseEditDialog() {
      this.$emit('closeDialog');
    },
  },
  computed: {
    _visible(){
      return this.visible;
    },
    mode(){
      if(!!this.postID)
        return "editPost";
      else
        return "writePost";
    },
    modeTitle(){
      if(!!this.postID)
        return "게시글 수정";
      else
        return "새 게시글";
    }
  },
};
</script>

<style scoped lang="less">

changeLocale
.title-input {
  margin-bottom: 20px;
}

</style>
