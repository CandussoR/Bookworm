<template>
  <dialog id="reading_modal" ref="reading_modal" class="modal">
      <div class="modal-box">
        <h3 class="text-lg font-bold text-center">{{ record ? 'Update a reading' : 'Add a reading' }}</h3>

        <div class="modal-action place-content-center">
          <form @submit.prevent="submitForm">
            <div class="flex flex-col gap-y-5">
              <!-- Search -->
              <CustomDatalist v-if="!selected" @selected="(b) => selected = b" />
              <!-- Display the title and authors when selected -->
              <div v-if="selected">
                <div id="title-container" class="indicator">
                  <span id="delete-badge" class="indicator-item badge badge-primary">
                    <img class="cursor-pointer" src="@/assets/delete.svg" alt="Delete" @click="selected = null">
                  </span>
                  <div dir="rtl" id="selected-book" class="bg-base-300 grid h-fit w-fit p-3 rounded place-items-center text-ellipsis lg:max-w-[250px] max-w-[150px]">
                    {{ selected.title }} ( {{ selected.author }} )
                  </div>
                </div>
              </div>

              <!-- Dates -->
              <div id="date-input">
                <div>
                  <label for="beginning-date" class="mr-2">Beginning : </label>
                  <input id="beginning-date" type="date" class="input" required
                    :max="new Date().toISOString().split('T')[0]" v-model="dateBeginning">
                </div>
                <div>
                  <label for="ending-date" class="mr-2">Ending : </label>
                  <input id="ending-date" type="date" class="input" :min="dateBeginning"
                    :max="new Date().toISOString().split('T')[0]" v-model="dateEnding">
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

            <div v-if="error" id="error">
              <p  class="text-error">{{error}}</p>
            </div>

            <!-- if there is a button in form, it will close the modal -->
            <button class="btn" type="submit" :disabled="isFormValid() && isValidDates(dateBeginning, dateEnding) ? false : true">
              Submit
            </button>
          </form>
        </div>
      </div>
    </dialog>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import CustomDatalist from './CustomDatalist.vue';

const emit = defineEmits(['submit'])
const { record } = defineProps({
    record : {
        type: Object,
        required : false
    }
})

// the whole book object selected
const selected = ref(null)

const dateBeginning = ref(null)
const dateEnding = ref(null)
const readingStatus = ref(1)
const error = ref(null)

onMounted(() => {
  if (!record) return;
  selected.value = { "title": record.title, "author": record.author }
  dateBeginning.value = record.beginning_date
  dateEnding.value = record.ending_date
  readingStatus.value = getReadingStatusValue(record.reading_status)
})

watch(readingStatus, nv => {
  if (nv !== 1 && !dateEnding.value) {
    dateEnding.value = getCurrentDate()
  }
})

function getReadingStatusValue(val) {
    const mapping = { "Reading" : 1, "Finished" : 2, "Partially Read" : 3, "On Hold" : 4, "Dropped" : 5}
    return mapping[val]
}


function submitForm() {
  if (!isFormValid()) return;

  const data = {
    [record? "reading_guid" : "ebook_guid"]: record? record.reading_guid : selected.value.ebook_guid,
    "beginning_date": dateBeginning.value,
    "ending_date": dateEnding.value,
    "reading_status": Number(readingStatus.value),
  }

    emit('submit', record ? 'update' : 'create', data)
}

function isFormValid() {
  // When the component is initialized, probably no date values but no error, so we just get out
  if (!dateBeginning.value && !dateEnding.value) {
    return false
  }

  if (readingStatus.value !== 1 && !dateEnding.value) {
    error.value = "This record must have an ending value."
    return false;
  }
  if (!isValidDates(dateBeginning.value, dateEnding.value)) {
    error.value = "Error in dates."
    return false
  }
  return true
}


function isValidDates(start, end) {
  if (start === null || (start && end && end < start)) {
    return false
  }
  
  const currentDate = getCurrentDate();
  if (end && end > currentDate) {
    return false
  }

  return true
}

function getCurrentDate() {
  const date = new Date();
  let day = date.getDate()
  let month = date.getMonth() + 1
  let year = date.getFullYear()
  return `${year}-${month}-${day}`
}
</script>

<style>

</style>