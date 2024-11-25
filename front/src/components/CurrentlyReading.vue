<template>
  <div class="collapse-content">
    <li v-if="currentlyReading">
      <i v-for="(e, i) in currentlyReading" :key="i">
        <span class="font-semibold">{{ e.title }}</span>, {{ e.author }} ;
      </i>
    </li>
    <button @click="openModal">Add a book...</button>

    <!-- Modal with form -->
    <dialog v-if="open" id="reading_modal" ref="reading_modal" class="modal">
      <div class="modal-box">
        <h3 class="text-lg font-bold text-center">Add a reading</h3>

        <div class="modal-action place-content-center">
          <form @submit="submitForm" method="dialog">
            <div class="flex flex-col gap-y-5">
              <!-- Search -->
               <CustomDatalist v-if="!selected" @selected="(b) => selected = b"/>
              <!-- Display the title and authors when selected -->
              <div v-if="selected">
                <div id="title-container" class="indicator">
                  <span id="delete-badge" class="indicator-item badge badge-primary"><img class="cursor-pointer"
                      src="@/assets/delete.svg" alt="Delete" @click="selected = null"></span>
                  <div id="selected-book" class="bg-base-300 grid h-fit w-fit p-3 rounded place-items-center">
                    {{ selected.title }} ( {{ selected.author }} )
                  </div>
                </div>
              </div>

              <!-- Dates -->
              <div id="date-input">
                <div >
                  <label for="beginning-date" class="mr-2">Beginning : </label>
                  <input id="beginning-date" type="date" class="input" required :max="new Date().toISOString().split('T')[0]"
                    v-model="dateBeginning">
                </div>
                <div>
                  <label for="ending-date" class="mr-2">Ending : </label>
                  <input id="ending-date" type="date" class="input" :min="dateBeginning" :max="new Date().toISOString().split('T')[0]"
                    v-model="dateEnding">
                </div>
              </div>

              <!-- Select status -->
              <div id="status-select" class="z-1">
                <label for="status">Status : </label>
                <select id="status" name="status" class="select" v-model="readingStatus">
                  <option value="1">Reading</option>
                  <option value="2">Finished</option>
                  <option value="3">Partially read</option>
                  <option value="4">On Hold</option>
                  <option value="5">Dropped</option>
                </select>
              </div>
            </div>
            <!-- if there is a button in form, it will close the modal -->
            <button class="btn" type="submit" :disabled="selected ? false : true">
              Submit
            </button>
          </form>
        </div>
      </div>
    </dialog>
  </div>

</template>

<script setup>
import CustomDatalist from './CustomDatalist.vue';
import axios from '../utils/apiRequester'
import { nextTick, onMounted, ref, watch } from 'vue'

let currentlyReading = ref([{"title" : "Test", "author": "Roro Canduss"}])
// flag for the opening of modal
const open = ref(false)

// the whole book object selected
const selected = ref(null)

const dateBeginning = ref(null)
const dateEnding = ref(null)
const readingStatus = ref(1)

watch(selected, nv => console.log("new value for selected", nv), {deep: true})

onMounted(async () => {
  try {
      let res = await axios.get('readings')
      if (res.data) {
          currentlyReading.value = res.data
      }
  } catch(error) {
      console.error(error)
  }
})

function openModal() {
  open.value = true
  nextTick(() => {
    const modal = document.getElementById('reading_modal')
    modal.showModal()
  })
}

async function submitForm() {
  if (!(isValidDates(dateBeginning.value, dateEnding.value))) {
    console.error("Wrong dates.")
    return
  }

  const data = {
    "ebook_guid": selected.value.ebook_guid,
    "beginning_date": dateBeginning.value,
    "ending_date": dateEnding.value,
    "reading_status": readingStatus.value,
  }
  
  try {
    const res = await axios.post("readings/active", data)
    if (res.status === 200) {
      if (currentlyReading.value) {
        currentlyReading.value.push(res.data)
      } else {
        currentlyReading.value = [res.data]
      }
    }
  } catch (error) {
    console.error(error)
  }
}


function isValidDates(startingDate, endingDate) {
  if (startingDate === null || (startingDate && endingDate && endingDate < startingDate)) {
    return false
  }

  const date = new Date();

  let day = date.getDate()
  let month = date.getMonth() + 1
  let year = date.getFullYear()
  let currentDate = `${year}-${month}-${day}`
  ;
  if (endingDate && endingDate > currentDate) {
    return false
  }

  return true
}

</script>

<style scoped></style>
