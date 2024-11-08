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
                    :tabindex="i"
                    @click.exact="handleRowSelect(i, path)"
                    @click.shift.exact="handleRowSelectFromLastOne(i)"
                    @click.ctrl.exact="handleRowSelect(i,path)"
                    @click.ctrl.shift="handleRowAdding(i,path)"
                    @keydown.shift="handleShift('down')"
                    @keyup.shift="handleShift('up')"
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
            <button id="edit" class="btn btn-neutral mr-1" @click="loadAndLaunchModal">Edit</button>
            <button id="delete" class="btn btn-neutral mr-1" @click="deleteBook">Delete</button>
            <button id="cancel" class="btn btn-neutral" @click="selected = []">Cancel</button>
        </div>

        <div v-if="open" >
            <MetadataEdit :ebooks="selectedFiles" :keys="keys" @updated="(u) => changeSelectedBooksMetadata(u)" />
        </div>

    </div>


</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { computed, onMounted, ref, watch, nextTick } from 'vue';
import axios from '@/utils/apiRequester'
import MetadataEdit from './MetadataEdit.vue';

const props = defineProps({
    ebooks : {
        required : false,
        type : Object
    }
})
const emit = defineEmits(['deleted', 'added', 'updated'])
const store = useAddingListStore()
// used to keep track of the index of selected files
const selected = ref([])
// used to keep track of the index when multiple click with shift
const lastSelectAtShift = ref(null)
// things sended to MetadataEdit
const selectedFiles = ref({})
const keys = computed(() => Object.keys(selectedFiles.value) || 0)
// books loaded in the table
const ebooks = computed(() => props.ebooks || store.addingList)
// controlling the opening of the modal
const open = ref(false)

onMounted(async () => {
    // just ensuring store.addingList is fed
    if (!props.ebooks) {
        await store.getAddingList()
    }
})

watch(lastSelectAtShift, (nv) => {
    if (nv === null) {
        console.log("shift key up, nullifying")
    } else {
        console.log("shift key down, last selected", nv)
    }
},
    {deep : true}
)

function handleShift(upOrDown) {
    console.log(upOrDown, lastSelectAtShift.value)
    if (upOrDown === "up" && lastSelectAtShift.value) {
        lastSelectAtShift.value = null;
        return;
    }
    if (upOrDown === "down" && ! lastSelectAtShift.value) {
        lastSelectAtShift.value = selected.value[selected.value.length - 1];
    }
}

/**
 * Controls the loading of MetadataEdit component and opens modal at DOM change
 **/
function loadAndLaunchModal() {
    open.value = true
    nextTick(() => {
        const modal = document.getElementById('edit_modal')
        modal.showModal()
    })
}

/**
 * Handles the addition of a row to selected and selectedFiles
 * @param {Number} i - index of the row clicked
 * @param {String} path - path of the file displayed in row
 **/
function handleRowSelect(i, path) {
    const arrIndex = selected.value.findIndex(el => el === i)
    if (arrIndex !== -1) {
        selected.value.splice(arrIndex, 1)
        delete selectedFiles.value[path]
        return
    }
    selected.value.push(i)
    selectedFiles.value[path] = store.addingList[path]
}

/**
 * Fired at shift+clic
 * @params {Number} selectedI - index of the row clicked
 **/
function handleRowSelectFromLastOne(selectedI) {
    // unselecting everything but the last selected
    selected.value = [ lastSelectAtShift.value || selected.value[selected.value.length - 1] ]
    let [bookPath, bookMeta] = Object.entries(ebooks.value)[selected.value[0]]
    selectedFiles.value = { [bookPath] : bookMeta }

    // Determining the order of iteration
    const lastSelectedGreater = selected.value[0] > selectedI;
    const ebooksEntriesSlice = lastSelectedGreater ? Object.entries(ebooks.value).slice(selectedI, selected.value[0] + 1) : Object.entries(ebooks.value).slice(selected.value[0], selectedI + 1) 
    
    if (lastSelectedGreater) {
        for (let i = selected.value[0] - 1 ; i >= selectedI ; i --) {
            selected.value.push(i);
        }
        ebooksEntriesSlice.forEach((path, meta) => {
            selectedFiles.value[path] = meta;
        })
        return
    }

    const ebooksEntriesSliceSorted = lastSelectedGreater ? ebooksEntriesSlice : ebooksEntriesSlice.toReversed()
    for (let i = selected.value[0] + 1; i <= selectedI; i++) {
        selected.value.push(i);
    }
    ebooksEntriesSliceSorted.forEach(([path, meta]) => {
        selectedFiles.value[path] = meta;
    })
}

/**
 * @param {Object} updates - the properties of the books that have been modified during edit, all strings
 **/
async function changeSelectedBooksMetadata(updates) {
    try {
        const res = axios.put('dragged', updates)
        console.log("received res", res)
        if (res.status === 200) {
            console.log("I'm changeSelectedBooksMetadata and I received my response", res.data)
            console.log("Emitting updated to the View now")
            emit('updated', res.data);
            await nextTick(() => {
                const modal = document.getElementById('edit_modal');
                modal.close();
            })
        }
    }
    catch(error) {
        console.error("An error occured when you tried to modify the data of the dragged books", error)
        // if error, should we store some kind of pending modifications somewhere ?
    }
}

async function deleteBook() {
    try {

        const res = await axios.delete('dragged', { data :{ "filepath" : Object.keys(selectedFiles.value) } })

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