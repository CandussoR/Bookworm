<template>
    <div>

        <div id="table-container" class="w-full p-5 overflow-x-auto pb-20">
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
                    <tr v-for="(e, path, i) in ebooks" :key="i" :tabindex="i" @click.exact="handleRowSelect(i, path)"
                        @click.shift.exact="handleRowSelectFromLastOne(i)" @click.ctrl.exact="handleRowSelect(i,path)"
                        @click.ctrl.shift="handleRowAdding(i,path)"
                        @keydown.shift="lastSelectAtShift ?? handleShift('down')"
                        @keyup.shift="!lastSelectAtShift ?? handleShift('up')"
                        :class="[selected.includes(i) ? '!bg-calm-green text-primary-content' : '']">

                        <td dir="rtl"
                            class="whitespace-nowrap overflow-hidden text-ellipsis lg:max-w-[250px] max-w-[150px]">{{
                            path
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



            <!-- Errors -->
            <details v-if="errorKeys.length" tabindex="0" class="mt-5 collapse bg-base-200 collapse-arrow">
                <summary class="collapse-title text-xl font-medium text-error">Errors</summary>
                <div class="collapse-content">
                    <div v-for="(e, path, i) in errors" :key="i">
                        <p>{{path}} : {{ e }}</p>
                    </div>
                </div>
            </details>

            <!-- Modal -->
            <div v-if="open">
                <EditDraggedMetadata :ebooks="selectedFiles" :keys="keys" @updated="(u) => changeSelectedBooksMetadata(u)" />
            </div>

        </div>

        <!-- Buttons -->
        <div v-if="keys.length" id="button-row" class="fixed bottom-0 left-0 w-full flex justify-center p-3 bg-base-200">
            <button id="add" alt="Add" class="btn btn-primary mr-2" @click="addBook">Add</button>
            <div id="edit-buttons" v-if="selected.length > 0">
                <button id="edit" class="btn btn-secondary mr-2" @click="loadAndLaunchModal">Edit</button>
                <button id="delete" class="btn btn-neutral mr-2" @click="deleteBook">Delete</button>
                <button id="cancel" class="btn btn-neutral" @click="selected = []">Cancel</button>
            </div>
        </div>
    </div>




</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { computed, onMounted, ref, watch, nextTick } from 'vue';
import axios from '@/utils/apiRequester'
import EditDraggedMetadata from './EditDraggedMetadata.vue';

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

const errors = ref({})
const errorKeys = computed(() => Object.keys(errors.value) || [])

onMounted(async () => {
    // just ensuring store.addingList is fed
    if (!props.ebooks) {
        await store.getAddingList()
    }
})

function handleShift(upOrDown) {
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
        ebooksEntriesSlice.forEach(([path, meta]) => {
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
        const res = await axios.put('dragged', updates)
        if (res.status === 200) {
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

async function addBook() {
    if (errorKeys.value) errors.value = {}

    const payload = {"isDragged" : true, "isMultiple" : null, "ebooks" : null}
    // returns empty if everything went well, else errors
    if (selected.value.length) {
        payload.isMultiple = selected.value.length > 1 ? true : false
        payload.ebooks = selectedFiles.value
    } else {
        payload.isMultiple = Object.keys(ebooks).length > 1 ? true : false
        payload.ebooks = ebooks
    }

    try {
        const res = await axios.post('ebooks', payload)
        if (res.status === 200) {
            res.data.success.forEach((p) => delete store.addingList[p])
            if (Object.keys(res.data.errors).length) {
                errors.value = res.data.errors
                console.log("some files have errors but oh well")
            }   

        }
    } catch (error) {
        console.log(error)
    }

    // if (res.errors) {
    //  emit('added', selectedFilesPath.value - errors)
    // } else {
    // emit('added', selectedFilesPath.value)
    // }

}
</script>