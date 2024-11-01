<template>
    <main class="flex flex-col align-center">
        <h1 class="text-center text-xl text-bold my-10">Drag & Drop</h1>
        <!-- Drag&Drop -->
        <div class="mt-5 bg-base-200 py-2 rounded">
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
        <p id="success" class="text-center text-success">{{success}}</p>
        <p id="error" class="text-center text-error">{{draggedError}}</p>

        <!-- Books added this session, open for review -->
        <div class="mt-5" ref="table">
            <h3 class="text-lg text-bold text-center" v-if="added && Object.keys(added).length > 0">Waiting for review</h3>

            <EditableMetadataTable v-if="added && Object.keys(added).length > 0" :ebooks="added" @deleted="deleteFromAdded($event)"/>
        </div>

    </main>
</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { listen } from '@tauri-apps/api/event';
import { ref, useTemplateRef, watch } from 'vue';
import axios from '@/utils/apiRequester';
import EditableMetadataTable from '@/components/EditableMetadataTable.vue';

const store = useAddingListStore()
const draggedError = ref(null)
const added = ref(null)
const success = ref(null)
const table = useTemplateRef("table")
const dropEvents = ref([])
const processingDropEvent = ref(null)

listen("tauri://drag-drop", async (event) => {
    // Couldn't prevent random firing of 10 events instead of one
    // So we'll put it all in some kind a queue thing and unqueue from there
    // This is shit though, but if it works it could be worse
    dropEvents.value.push(event)

    if (processingDropEvent.value) {
        return ;
    }
    processingDropEvent.value = true
})

watch(processingDropEvent, async (val, oldVal) => {
    if (!val) return;
    await handleDrop(dropEvents.value[0].payload.paths)
    const nextEvent = checkEventsHaveDifferentPaths()

    while (nextEvent) {
        await handleDrop(nextEvent.payload.paths)
        nextEvent = checkEventsHaveDifferentPaths()
    }

    processingDropEvent.value = false
})


async function handleDrop(paths) {

    try {
        const res = await axios.post('dragged', { "filepaths": paths })

        if (!res.status == 200) {
            draggedError.value = res.data
            return
        }

        setTimeout(() => success.value = '', 2000)
        if (!Object.keys(res.data).length) {
            success.value = "Books already in the database or already waiting for review."
            return
        }

        success.value = "Books added to the database."

        const resDataKeys = Object.keys(res.data)

        if (!added.value) {
            added.value = res.data
        } else {
            resDataKeys.forEach(p => {
                added.value[p] = res.data[p]
            })
        }
        
        resDataKeys.forEach(p => {
            store.addingList[p] = res.data[p]
        })
        table.value.focus()
    } catch (error) {
        draggedError.value = error
        setTimeout(() => draggedError.value = '', 5000)
    }
}


function checkEventsHaveDifferentPaths() {
    const handled = dropEvents.value.splice(0,1);
    while (dropEvents.value.length > 0) {
        const nextEvent = dropEvents.value.splice(0,1);
        // Slow as hell, won't bark while it works
        if (JSON.stringify(handled.payload.paths) === JSON.stringify(nextEvent.payload.paths)) {
            continue;
        }
        return nextEvent
    }
    return null
}

function deleteFromAdded(paths) {
    paths.forEach(element => {
       delete added.value[element]
    });
    if (!Object.keys(added).length) added.value = null
}
</script>

<style>
#sucess:empty,
#error:empty {
    display : none;
}
</style>