<template>
  <div :id="ebookProperty + '-input-with-chip'">

    <input :id="ebookProperty" :ref="ebookProperty + 'ref'" :list="ebookProperty + '-search-result'"
      @input="(event) => debounce(ebookProperty, event.target.value)" @keydown.enter="addChip()" class="input"
      :name="ebookProperty" type="text" :required="required" minlength="1" maxlength="200"
      :placeholder="computedPlaceholder" />

    <datalist :id="ebookProperty + '-search-result'">
      <option v-for="(it, i) in searchResult" :key="i" :value="it"></option>
    </datalist>

    <div :id="ebookProperty + '-chips'">
      <div id="chip-container" class="indicator" v-for="(chip, i) in chips" :key="i">
        <span id="chip-delete-badge" class="indicator-item badge badge-primary"><img class="cursor-pointer"
            src="@/assets/delete.svg" alt="Delete" @click="deleteChip(i)" /></span>
        <div :id="chip + '-chip'" class="bg-base-300 grid h-fit w-fit p-3 rounded place-items-center">{{ chip }}</div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onUnmounted, ref, useTemplateRef, watch} from 'vue'
import axios from '@/utils/apiRequester'

const { ebookProperty, placeholder, required } = defineProps({
  'ebook-property': String,
  'placeholder': {
    required: false,
    type: String
  },
  'required': Boolean
})
const computedPlaceholder = computed(() => placeholder && placeholder !== "Various" ? '' : placeholder)
const emit = defineEmits(['updated'])
const timer = ref(null)
const hasReceivedResponse = ref(false)
const searchResult = ref([])
const inputRef = useTemplateRef(ebookProperty + "ref")
const chips = ref([])

// still don't know how placeholder isn't already a value when passed, forced to do this for now
watch(() => placeholder, () => getInitialChip(), {once: true})

onUnmounted(() => searchResult.value = null)

function getInitialChip() {
  if (placeholder && placeholder !== "Various") {
    chips.value = placeholder.split(', ')
  }
}

function addChip() {
  if (inputRef.value.value ) {
    chips.value.push(inputRef.value.value)
    inputRef.value.value = null
    emit("updated", ebookProperty, chips.value)
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
  timer.value = setTimeout(async () => await searchFor(key, val), 500)
}

function deleteChip(i) {
  chips.value.splice(i, 1)
  emit("updated", ebookProperty, chips.value)
}

async function searchFor(k, v) {
  console.log(k, v)
  try {
    const res = await axios.get('search', { params : { [k]: v } })
    if (res.status === 200) {
      searchResult.value = res.data
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<style></style>
