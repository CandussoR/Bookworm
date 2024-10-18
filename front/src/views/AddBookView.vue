<template>
    <main class="flex flex-col align-center">
    <!-- <div class="flex flex-col h-screen flew-grow justify-center items-center overflow-scroll"> -->
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
                    <label for="abs-path">Absolute path of directory :</label>
                    <input id="abs-path" name="abs-path" type="text" required minlength="3" v-model="absPath">

                    <div @drop.prevent="handleDrop" @dragenter="handleDragEnter" @dragover.prevent="" class="flex flex-col items-center justify-center py-10 text-center">
                        <svg class="w-6 h-6 mr-1 text-current-50" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <p class="m-0">Drag your files here or click in this area.</p>
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

        <dialog id="modal" ref="modal" class="modal">
            <div class="modal-box">
                <p v-if="success" id="success" class="text-center text-success">The book has been added to the database.</p>
                <p v-else-if="draggedError" id="error" class="text-center text-error">An error has occured.</p>
            </div>
        </dialog>

    <!-- </div> -->
</main>
</template>

<script setup>
import SearchFormInput from '@/components/SearchFormInput.vue';
import axios from '@/utils/apiRequester'
import { useTemplateRef, ref, onMounted } from 'vue';

const modal = useTemplateRef('modal')
const success = ref(0)
const absPath = ref('')
const absFilePaths = ref([])
const choice = ref(null)
const draggedError = ref(false)

// import { listen } from '@tauri-apps/api/event';

// onMounted(() => {
//   listen("tauri://drag-drop", (event) => {
//     console.log("Tauri file drop event", event);
//     if (event.payload && Array.isArray(event.payload)) {
//       event.payload.forEach(filePath => {
//         console.log("File dropped:", filePath);
//         absFilePaths.value.push(filePath);
//       });
//     }
//   });
// });

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
    // const res = await axios.post('ebooks', ebook)
    const res = {"status" : 201}
    if (res.status === 201) {
        success.value = 1
    }
    modal.value.showModal()
    setTimeout(() => modal.value.close(), 1000)
}

function handleDragEnter(event) {
    console.log("Entered the drag !", event, event.dataTransfer.types, event.dataTransfer.kind)
    event.preventDefault()
}

async function handleDrop(event) {
    event.preventDefault()
    // console.log(event.dataTransfer.items.length)
    // console.log(event.dataTransfer.items)
    console.log("dropped this, king", event)
    if (!event.dataTransfer.items.length) {
        console.log("Dropped event but nothing dropped ?!")
        return
    }

    // console.log("items are", Array.from(event.dataTransfer.items))
    Array.from(event.dataTransfer.items).forEach((el) => {
        // console.log("This item is a", el.kind, "and its MIME type is", el.type)
        // console.log(el)
        const element = el.webkitGetAsEntry()
        // console.log("element as webkitGetEntry", element)
        let join_char = absPath.value.endsWith('/') || absPath.value.endsWith('\\') ? '' : '/'
        absFilePaths.value.push([absPath.value, element.name].join(join_char))
    })

    const res = await axios.post('draggable', {"filepaths" : absFilePaths.value})
    if (res.status_code !== 200) {
        draggedError.value = true
    }

}
</script>