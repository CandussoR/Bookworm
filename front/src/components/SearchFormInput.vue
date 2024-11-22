<template>
  <div>
    <input :id="ebookProperty" :list="ebookProperty + '-search-result'"
    @input="(event) => debounce(ebookProperty, event.target.value)"
      class="input placeholder:italic" :name="ebookProperty" type="text"
      :required="required" minlength="1" maxlength="200" :placeholder="placeholder" />
    <datalist v-if="ebookProperty === 'publisher'" :id="ebookProperty + '-search-result'">
      <option v-for="(it, i) in searchResult" :key="i" :value="it"></option>
    </datalist>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const { ebookProperty, placeholder, required } = defineProps({
  'ebook-property': String,
  placeholder: {
    required: false,
    type: String
  },
  required: Boolean
})

const timer = ref(null)

const searchResult = ref([])

function debounce(key, val) {
  if (key !== 'publisher') return

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

async function searchFor(k, v) {
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
