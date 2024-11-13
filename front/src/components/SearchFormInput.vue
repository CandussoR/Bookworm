<template>
  <div>
    <input :id="ebookProperty" :list="ebookProperty + '-search-result'"
      class="input" :name="ebookProperty" type="text"
      :required="required" minlength="1" maxlength="200" :placeholder="placeholder" />
  </div>
</template>

<script setup>
const { ebookProperty, placeholder, required } = defineProps({
  'ebook-property': String,
  placeholder: {
    required: false,
    type: String
  },
  required: Boolean
})
</script>

<style></style>
