<template>
  <main v-if="ebooks">
    <h1 class="text-5xl text-center my-10">Your books</h1>
    <!-- DaisyUI Component -->
    <div class="overflow-x-auto">
      <table class="table table-zebra">
        <!-- head -->
        <thead>
          <tr>
            <!-- <th></th> -->
            <th></th>
            <th>Title</th>
            <th>Author</th>
            <th>Year of Publication</th>
            <th>Publisher</th>
            <th>Genre</th>
            <th>Theme</th>
          </tr>
        </thead>
        <TableBody v-if="ebooks" :ebooks="ebooks" @get-ebooks-for="(key, value) => seeBooksFor(key, value)"
          @update-selection="(data) => handleSelection(data)" />
      </table>

      <!-- Modal -->
      <div v-if="open">
        <EditDatabaseData :ebooks="selectedBooks" :keys="keys" @updated="(u) => updateBooks(u)" />
      </div>
      <!-- Pagination -->
      <Pagination class="align-right" :number-of-pages=numberOfPages @get-page="(num) => getPage(num)" />

    </div>


    <!-- Buttons -->
    <div v-if="selected.length" id="button-row"
      class="fixed bottom-0 left-0 w-full flex justify-center p-3 bg-base-200">
      <div id="edit-buttons" v-if="selected.length > 0">
        <button id="edit" class="btn btn-secondary mr-2" @click="loadAndLaunchModal">Edit</button>
        <button id="delete" class="btn btn-neutral mr-2" @click="deleteBook">Delete</button>
        <button id="cancel" class="btn btn-neutral" @click="selected = []">Cancel</button>
      </div>
    </div>
  </main>
  <main v-else class="h-screen relative">
    <h1 class="text-5xl text-center my-10">Your books</h1>
    <span class="absolute bottom-1/2 left-1/2 loading loading-ring loading-lg"></span>
  </main>
</template>

<script setup>
import { computed, ref, nextTick } from 'vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TableBody from '@/components/TableBody.vue'
import EditDatabaseData from '@/components/EditDatabaseData.vue'
import Pagination from '@/components/Pagination.vue'
import { ebookStore } from '@/stores/ebooks.js'
import axios from '@/utils/apiRequester'

let router = useRouter()
const store = ebookStore()
let ebooks = ref(null)
let selected = ref([])
let selectedBooks = computed(() => selected.value.map((i) => ebooks.value[i]))
const open = ref(false)
const numberOfPages = ref(null)

onMounted(async () => {
  if (!store.ebooks) {
    await store.index()
  }
  numberOfPages.value = calculateNumberOfPages()
  getPage(1)
})

function seeBooksFor(key, value) {
  // Router sur une autre page qui affiche les ebooks liés à la clé sélectionnée.
  router.push({ name: `ebooks`, params: { key: key, value: value } })
}

function handleSelection(data) {
  selected.value = data
}

// Opens the modal for potential edit
function loadAndLaunchModal() {
  open.value = true
  nextTick(() => {
    const modal = document.getElementById('edit_modal')
    modal.showModal()
  })
}


async function updateBooks(updatedData) {
  try {
    const res = await axios.put('ebooks', { "updates": updatedData })
    if (res.status === 200) {
      res.data.forEach((b) => { store.ebooks[store.ebooks.find((sE) => sE.ebook_guid === b.ebook_guid)] = b })
      ebooks.value = store.ebooks
      nextTick(() => {
        const modal = document.getElementById('edit_modal')
        modal.close()
      })
    }
  } catch (error) {
    console.error(error)
  }
}

async function deleteBook() {
  try {
    const guids = selected.value.map((i) => store.ebooks[i].ebook_guid)
    const res = await axios.delete('ebooks', { data: { "guids": guids } })
    if (res.status == 200) {
      guids.forEach(g => store.ebooks.splice(store.ebooks.findIndex((b) => b.ebook_guid === g), 1))
      ebooks.value = store.ebooks
    }
  }
  catch (error) {
    console.error(error)
  }
}

function calculateNumberOfPages() {
  return store.ebooks.length / import.meta.env.VITE_PAGE
}


function getPage(num) {
  const beginning = (num - 1) * import.meta.env.VITE_PAGE
  ebooks.value = store.ebooks.slice(beginning, beginning + import.meta.env.VITE_PAGE)
}
</script>