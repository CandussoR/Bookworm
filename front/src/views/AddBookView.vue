<template>
    <main class="flex flex-col align-center">
        <h3 class="text-lg font-bold text-center">New Book</h3>

        <div class="flex w-full" v-if="!choice">
            <div class="card bg-base-300 rounded-box grid h-20 flex-grow place-items-center" @click="choice = 'drag&drop'">
                <p>Drag&Drop as many files as you want</p>
            </div>
            
            <div class="divider divider-horizontal">OR</div>

            <div class="card bg-base-300 rounded-box grid h-20 flex-grow place-items-center" @click="choice = 'manually'">
                <p>Add books manually</p>
            </div>
        </div>

        <div class="flex w-full" v-else>
            
                <div id="drag-drop-block" v-if="choice == 'drag&drop'">

                    <div @drop.prevent="handleDrop" @dragenter.prevent="handleDragEnter" @dragover.prevent class="flex flex-col items-center justify-center py-10 text-center bg-base-200">
                        <svg class="w-6 h-6 mr-1 text-current-50" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <p class="m-0 p-2">Drag your files here or click in this area.</p>
                    </div>
                </div>

            <div v-else-if="choice == 'manually'" class="card bg-base-300 rounded-box grid h-20 flex-grow place-items-center">
                <form @submit.prevent="submit" class="flex flex-col">
                    <label id="title">Title</label>
                    <SearchFormInput ebook-property="title" autofocus required/>

                    <label id="author">Author</label>
                    <SearchFormInput ebook-property="author" required/>

                    <label id="publisher">Publisher</label>
                    <SearchFormInput ebook-property="publisher" required/>

                    <label id="theme">Themes</label>
                    <SearchFormInput ebook-property="theme"/>

                    <label id="genre">Genres</label>
                    <SearchFormInput ebook-property="genre"/>

                    <button class="my-4 btn btn-outline btn-neutral" type="submit">Send</button>
                </form>
            </div>
        </div>

        <!-- Success info -->
        <p v-if="success" id="success" class="text-center text-success">The book has been added to the database.</p>
        <p v-else-if="draggedError" id="error" class="text-center text-error">An error has occured. {{draggedError}}</p>

        <div v-if="added">
            <h3 class="text-bold" v-if="added">Waiting for review</h3>

            <ul>
                <li v-for="(ebook,i) in added" :key="i">
                    {{ebook}}
                </li>
            </ul>
        </div>

        

</main>
</template>

<script setup>
import SearchFormInput from '@/components/SearchFormInput.vue';
import axios from '@/utils/apiRequester'
import { listen } from '@tauri-apps/api/event';
import { ref } from 'vue';

const success = ref(0)
const absFilePaths = ref([])
const choice = ref(null)
const draggedError = ref('')
const added = ref(null)


async function submit(event) {
    const elements = event.target.elements
    const ebook = {
        "title" : elements.namedItem("title").value,
        "author" : elements.namedItem("author").value,
        "publisher" : elements.namedItem("publisher").value,
        "theme" : elements.namedItem("theme").value,
        "genre" : elements.namedItem("genre").value
    }
    if (ebook.theme.includes(', ')) {
        ebook.theme = ebook.theme.split(", ")
    }
    if (ebook.genre.includes(', ')) {
        ebook.genre = ebook.genre.split(', ')
    }

    try {
        // const res = await axios.post('ebooks', ebook)
        const res = {"status" : 201}
        if (res.status === 201) {
            success.value = 1
            setTimeout(() => success.value = 0, 1000)
        }
    } catch(error) {
        draggedError.value = str(e)
        setTimeout(() => draggedError.value = '', 5000)
    }
    
}

function handleDragEnter(event) {
    event.preventDefault()
}

listen("tauri://drag-drop", async (event) => {

    console.log("Tauri file drop event", event);
    console.log("Event payload", event.payload);
    console.log("File paths", event.payload.paths);
    const dragPaths = event.payload.paths;
    if (!absFilePaths.value.length) {
        absFilePaths.value = dragPaths;
    } else {
        for (let i=0; i < dragPaths.length; i++) {
            absFilePaths.value.push(dragPaths[i])
        }
    }

    try {
        const res = await axios.post('dragged', {"filepaths" : dragPaths})
        if (res.status === 200) {
            success.value = 1
            setTimeout(() => success.value = 0, 1000)
            if (!added.value) added.value = res.data
            else {
                for (let i=0; i < ref.data.length; i++) {
                    added.value.push(res.data[i])
                }
            }
        }
    } catch(error) {
        draggedError.value = error
        setTimeout(() => draggedError.value = '', 5000)
    }
});
</script>