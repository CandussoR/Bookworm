<template>
  <div>
    <input :ref="ebookProperty + 'ref'" :id="ebookProperty" :list="ebookProperty + '-search-result'"
      @input="(event) => debounce(ebookProperty, event.target.value)" @keydown.space="addChip()" class="input"
      :name="ebookProperty" type="text" :required="required" minlength="1" maxlength="200" :placeholder="placeholder" />
    <datalist :id="ebookProperty + '-search-result'">
      <option v-for="(it, i) in searchResult" :key="i" :value="it"></option>
    </datalist>
    <div>
      <div class="indicator" v-for="(chip, i) in chips" :key="i">
        <span class="indicator-item badge badge-primary"><img class="cursor-pointer" src="@/assets/delete.svg"
            alt="Delete" @click="console.log('clicked', i, chip)" /></span>
        <div class="bg-base-300 grid h-32 w-32 place-items-center">{{ chip }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, useTemplateRef, watch} from 'vue'

const { ebookProperty, placeholder, required } = defineProps({
  'ebook-property': String,
  'placeholder': {
    required: false,
    type: String
  },
  'required': Boolean
})
const timer = ref(null)
const hasReceivedResponse = ref(false)
const searchResult = ref([])
const inputRef = useTemplateRef(ebookProperty + "ref")
const chips = ref([])

// still don't know how placeholder isn't already a value when passed, forced to do this for now
watch(() => placeholder, () => getInitialChip())

function getInitialChip() {
  if (placeholder && placeholder !== "Various") {
    chips.value = placeholder.split(', ')
  }
}

function addChip() {
  if (inputRef.value.value && inputRef.value.value !== ' ') {
    chips.value.push(inputRef.value.value.split(' ')[0])
    inputRef.value.value = null
  }
}

function debounce(key, val) {
  if (searchResult.value && searchResult.value.includes(val)) {
    searchResult.value = []
    return
  }

  // On each input, we delete the timer set to only send a request with the latest input
  if (timer.value) {
    clearTimeout(timer.value)
  }
  // We also want to reset the received_response since we have not yet make the request
  hasReceivedResponse.value = 0

  if (val == '') {
    searchResult.value = []
    return
  }
  // searchForBooks only gets called when user stops typing for 500ms
  timer.value = setTimeout(() => searchFor(key, val), 500)
}

function searchFor(k, v) {
  if (v === 'test') {
    searchResult.value = ['test', 'test2', 'test3']
  }
}
</script>

<style></style>
