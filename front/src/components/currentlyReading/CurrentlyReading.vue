<template>
  <div class="collapse-content  flex flex-col h-full">
    <ul v-if="currentlyReading">
      <li v-for="(e, i) in currentlyReading" :key="i" @mouseover="changeDisplay(i)" @mouseleave="display = null"
        class="relative hover:bg-base-50">
        <img v-if="display === i" class="cursor-pointer absolute -right-4 top-0 bg-base-100 rounded-lg"
          src="@/assets/edit.svg" alt="More actions" @click="openModal(e)" @mouseover.stop @mouseenter.stop />
        <p class="inline-block"><span class="font-semibold">{{ e.title }}</span>, {{ e.author }} ;</p>
      </li>
    </ul>
    <div class="flex justify-center items-center h-full">
      <button class="btn" @click="openModal(undefined)">Add a book...</button>
    </div>
    <!-- Modal with form -->
    <ReadingModal v-if="open && dataInModal" :record="dataInModal"
      @submit="(operation, form) => submitForm(operation, form)" />
    <ReadingModal v-else-if="open && !dataInModal" @submit="(operation, form) => submitForm(operation, form)" />
  </div>

</template>

<script setup>
import axios from '../../utils/apiRequester'
import { nextTick, onMounted, ref } from 'vue'
import ReadingModal from './ReadingModal.vue';

let currentlyReading = ref(null)
// flag for the opening of modal
const open = ref(false)


const display = ref(null)
const dataInModal = ref(null)

onMounted(async () => {
  try {
      let res = await axios.get('readings/active')
      if (res.data) {
          currentlyReading.value = res.data
      }
  } catch(error) {
      console.error(error)
  }
})

function openModal(data) {
  dataInModal.value = data
  open.value = true
  nextTick(() => {
    const modal = document.getElementById('reading_modal')
    modal.showModal()
  })
}

async function submitForm(operation, data) {
  debugger
  try {
    let res = null

    if (operation === 'create') {
      res = await axios.post("readings/active", data)
    } else if (operation === 'update') {
      res = await axios.put("readings", data)
    }

    if (res.status === 200) {
      currentlyReading.value = res.data
      open.value = false
    }

  } catch (error) {
    console.error(error)
  }
}


function changeDisplay(i) {
  if (!display.value) display.value = i
}

</script>

<style scoped></style>
