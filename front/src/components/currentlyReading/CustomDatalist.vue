
<template>
  <div id="name-input" class="dropdown dropdown-open">
    <label for="book-title-search" class="block text-gray-700 mb-2">Search:</label>
    <input id="book-title-search" @input="handleInput" class="input input-bordered w-full placeholder:italic"
      placeholder="Search for a book..." type="text" />
    <ul v-if="searchResults.length > 0"
      class="dropdown-content menu bg-base-100 rounded-box z-[1] w-full p-2 shadow border border-gray-300">
      <li v-for="(result, i) in searchResults" :key="i" @click="select(result)" @keydown.enter="select(result)"
        class="cursor-pointer menu-item">
        <!-- Can't make the items to lighten up without the a on hover -->
        <a>
          {{ result.title + ' (' + result.author + ')' }}
        </a>
      </li>
      <li v-if="searchResults.length === 0" class="px-4 py-2 text-gray-500">
        No results found
      </li>
    </ul>
  </div>
</template>

<script setup>
// The reason for this very component is the separation of data displayed and data actually sent as selected.
// It is meant to deal with case where multiple self title
import { ref } from 'vue';
import axios from '@/utils/apiRequester';

const emit = defineEmits(['selected'])

// flag for debounce
const timer = ref(null)

const showDropdown = ref(false)

const searchResults = ref([])

function handleInput(event) {
  const val = event.target.value

  // If there is no search results, we do the search
  if (!searchResults.value.length) {
    debounce(val)
    return
  }

  //
  if (searchResults.value.includes(val)) {
    select(val)
    return
  }

}

function debounce(val) {
  // On each input, we delete the timer set so we only send a request with the latest input
  if (timer.value) {
    clearTimeout(timer.value)
  }

  // Clearing search results
  if (searchResults.value.length || val == '') {
    searchResults.value = []
  }

  if (val == '') {
    return
  }

  timer.value = setTimeout(async () => await searchTitle(val), 500)
}

async function searchTitle(s) {
    try {
        const res = await axios.get(`ebooks?search=${s}`)
        if (res.status === 200) {
          searchResults.value = res.data
        }
    } catch (error) {
        console.error(error)
    }
}

function select(book) {
  showDropdown.value = false
  emit('selected', book)
}
</script>

<style>

</style>