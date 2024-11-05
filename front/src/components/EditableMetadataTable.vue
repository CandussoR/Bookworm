<template>

    <div id="table-container" class="w-full p-5 overflow-x-auto">
        <table id="metadata-table" class="table table-zebra min-w-full">
            <thead>
                <tr>
                    <th scop="col">Path</th>
                    <th scop="col">Title</th>
                    <th scop="col">Author</th>
                    <th scop="col">Year_of_publication</th>
                    <th scop="col">Publisher</th>
                    <th scop="col">Genre</th>
                    <th scop="col">Theme</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(e, path, i) in ebooks" :key="i" 
                    @click.exact="handleRowSelect(i, path)"
                    @click.shift="handleRowSelectFromLastOne(i)"
                    @click.ctrl="handleRowSelect(i,path)"
                    :class="[selected.includes(i) ? '!bg-calm-green text-primary-content' : '']">
                    <td dir="rtl"
                        class="whitespace-nowrap overflow-hidden text-ellipsis lg:max-w-[250px] max-w-[150px]">{{ path
                        }}</td>

                    <td> {{ e. title }} </td>

                    <td>
                        <span v-for="(a, i) in e.author" :key="a">
                            {{ i === e.author.length - 1 ? a : a+ ', ' }}
                        </span>
                    </td>

                    <td>{{ e.year_of_publication }}</td>

                    <td>{{ e.publisher }}</td>

                    <td v-if="e.genre">
                        <span v-for="(g, j) in e.genre" :key="g">
                            {{ j === e.genre.length - 1 ? g : g + ', ' }}
                        </span>
                    </td>
                    <td v-else class="text-centered">
                        -
                    </td>

                    <td v-if="e.theme">
                        <span v-for="(t, j) in e.theme" :key="t">
                            {{ j === e.theme.length - 1 ? t : t + ', ' }}
                        </span>
                    </td>
                    <td v-else class="text-centered">-</td>
                </tr>
            </tbody>
        </table>

        <div id="button-row" v-if="selected.length > 0" class="flex justify-center">
            <button id="edit" class="btn btn-neutral mr-1" onclick="edit_modal.showModal()">Edit</button>
            <button id="delete" class="btn btn-neutral mr-1" @click="deleteBook">Delete</button>
            <button id="cancel" class="btn btn-neutral" @click="selected = []">Cancel</button>
        </div>

        <div v-if="keys.length">
            <MetadataEdit :ebooks="selectedFiles" :keys="keys"/>
        </div>

    </div>


</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { computed, onMounted, ref } from 'vue';
import axios from '@/utils/apiRequester'
import MetadataEdit from './MetadataEdit.vue';

const store = useAddingListStore()
const selected = ref([])
const selectedFiles = ref({})
const keys = computed(() => Object.keys(selectedFiles.value))

const error = ref('')
// const resReceived = ref(false)
const props = defineProps({
    ebooks : {
        required : false,
        type : Object
    }
})
const emit = defineEmits(['deleted', 'added'])

const ebooks = computed(() => props.ebooks || store.addingList)

onMounted(async () => {
    if (!props.ebooks) {
        await store.getAddingList()
    }
})

function handleRowSelect(i, path) {
    const arrIndex = selected.value.findIndex(el => el === i)
    if (arrIndex !== -1) {
        selected.value.splice(arrIndex, 1)
        delete selectedFiles.value[path]
        // selectedFilesPath.value.splice(arrIndex, 1)
        return
    }

    selected.value.push(i)
    selectedFiles.value[path] = store.addingList[path]
}

function handleRowSelectFromLastOne(selectedI) {
    let keys = props.ebooks ? Object.keys(props.ebooks) : Object.keys(store.addingList);
    
    const arrIndex = selected.value.findIndex(el => el === selectedI)
    const lastSelected = selected.value.length ? selected.value[selected.value.length - 1] : 0;

    if (arrIndex !== -1 && arrIndex < selected.value.length - 1) {
        selected.value.splice(arrIndex +1, selected.value.length - 1 - arrIndex)
        const paths = keys.slice(arrIndex,selected.value.length - 1 - arrIndex) 
        paths.forEach((p) => delete selectedFiles.value[p])
        // selectedFilesPath.value.splice(arrIndex +1, selected.value.length - 1 - arrIndex)
        return
    }

    for (let i = lastSelected ; i <= selectedI ; i++) {
        if (selected.value.includes(keys[i])) continue;
        selected.value.push(i);
        // selectedFilesPath.value.push(keys[i].path);
    }
    const paths = keys.slice(arrIndex,lastSelected - selectedI) 
    paths.forEach((p) => { 
        if (!(p in selectedFiles.value)) {
        selectedFiles.value[p] = store.addingList[p]
        }
    })
}

async function deleteBook() {
    try {
        const res = await axios.delete('dragged', { data :{ "filepath" : selectedFiles.value } })

        if (res.status == 200) {
            if (props.ebooks) {
                emit("deleted", selectedFiles.value)
                return
            }

            // Updating store if we're not in the DragDrop view, else no use
            selectedFiles.value.forEach(element => {
                if (element in store.addingList) {
                    delete store.addingList[element]
                }
            }
        );

            selectedFiles.value = []
        }
    } catch (error) {
        error.value = error
    }
}

function addBook() {
    console.log("we dummy add book")
    // returns empty if everything went well, else errors
    // const res = await axios.post('ebooks', {"ebooks" : ... })

    // if (res.errors) {
    //  emit('added', selectedFilesPath.value - errors)
    // } else {
    // emit('added', selectedFilesPath.value)
    // }

}
</script>