<template>
  <div class="multipane-resizer">
    <slot></slot>
  </div>
</template>
<script>
import Vue from 'vue';

export default Vue.component('MultipaneResizer', {
  template: '<div class="multipane-resizer"><slot></slot></div>',
});
</script>
<style scoped>
.multipane-resizer.hide {
  display: none;
}
</style>
