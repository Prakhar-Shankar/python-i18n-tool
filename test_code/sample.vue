<template>
  <div class="sample-component">
    <h1>{{ $t('header.title') }}</h1>
    <p>{{ $t('header.subtitle') }}</p>
    
    <div class="content">
      <p>{{ $t('content.paragraph') }}</p>
      <button>{{ $t('button.submit') }}</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SampleComponent',
  methods: {
    showGreeting() {
      alert(this.$t('greeting'));
      console.log(this.$t('user.name'));
    }
  }
}
</script>

<style scoped>
.sample-component {
  padding: 20px;
}
</style> 