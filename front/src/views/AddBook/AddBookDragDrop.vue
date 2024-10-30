<template>
    <main class="flex flex-col align-center">
        <!-- Drag&Drop -->
        <div @drop.prevent="handleDrop" @dragenter.prevent="handleDragEnter" @dragover.prevent class="mt-5 bg-base-200 py-2 rounded">
            <div id="drag-drop-inside" class="flex flex-col border-2 rounded m-5 p-10 items-center justify-center text-center">
                <svg class="w-8 h-8 mr-1 text-current-50" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="m-0 p-2">Drag your files here or click in this area.</p>
            </div>
        </div>


        <!-- Success info -->
        <p id="success-test" class="text-center text-success">{{successTest}}</p>
        <!-- <p v-else-if="draggedError" id="error" class="text-center text-error">An error has occured. {{draggedError}}</p> -->

        <!-- Books added this session, open for review -->
        <div v-if="added">
            <h3 class="text-bold" v-if="added">Waiting for review</h3>

            <EditableMetadataTable :ebooks="added"/>
        </div>

    </main>
</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { listen } from '@tauri-apps/api/event';
import { ref } from 'vue';
import axios from '@/utils/apiRequester';
import EditableMetadataTable from '@/components/EditableMetadataTable.vue';

const store = useAddingListStore()
const dropTriggered = ref(false)
const dropTriggeredTimeout = ref(null)
const draggedError = ref(null)
const added = ref(null)
const successTest = ref(null)

listen("tauri://drag-drop", async (event) => {
    if (dropTriggered.value) return;

    handleDropTriggered()

    handleDrop(event.payload.paths);
})

/**
 * Sort of a debounce function to limit the number of requests to the back
 * for each drop to one.
 **/
 function handleDropTriggered() {
    dropTriggered.value = true
    if (dropTriggeredTimeout.value) {
        clearTimeout(dropTriggeredTimeout.value)
    }
    setTimeout(() => dropTriggered.value = false, 1000)
}


async function handleDrop(paths) {

    try {
        const res = await axios.post('dragged', {"filepaths" : paths})
        console.log(res)

        if (res.status === 200) {
            console.log(res)
            setTimeout(() => successTest.value = null, 2000)
            if (!res.data.length) {
                // success.value = 2
                return
            }

            if (!added.value) {
                added.value = res.data
                // success.value = 1
                successTest.value = "Yup"
                for (let i=0; i < ref.data.length; i++) {
                    store.addingList.push(res.data[i])
                } 
                return
            }

            for (let i=0; i < ref.data.length; i++) {
                added.value.push(res.data[i])
                store.addingList.push(res.data[i])
            }
        }
    } catch(error) {
        // draggedError.value = error
        // setTimeout(() => draggedError.value = '', 5000)
    }
}
</script>

<style>
.sucess-test:empty {
    display : none;
}
</style>