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
                <tr v-for="(e, path, i) in ebooks" :key="i" @click="selectRow(i, path)"
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
            <button id="edit" class="btn btn-neutral mr-1">Edit</button>
            <button id="delete" class="btn btn-neutral mr-1" @click="deleteBook">Delete</button>
            <button id="cancel" class="btn btn-neutral" @click="selected = []">Cancel</button>
        </div>
    </div>


</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';
import { computed, onMounted, ref } from 'vue';
import axios from '@/utils/apiRequester'

const store = useAddingListStore()
const selected = ref([])
const selectedFilesPath = ref([])
const error = ref('')
const props = defineProps({
    ebooks : {
        required : false,
        type : Object
    }
})

const ebooks = computed(() => props.ebooks || store.addingList)

onMounted(async () => {
    await store.getAddingList()
})

function selectRow(i, path) {
    const arrIndex = selected.value.findIndex(el => el === i)
    if (arrIndex !== -1) {
        selected.value.splice(arrIndex, 1)
        selectedFilesPath.value.splice(arrIndex, 1)
        return
    }

    selected.value.push(i)
    selectedFilesPath.value.push(path)
}

async function deleteBook() {
    try {
        console.log("selectedFilesPath that I am sending", selectedFilesPath.value)
        const res = await axios.delete('dragged', { data :{ "filepath" : selectedFilesPath.value } })
        if (res.status == 200) {
            // Updating store
            selectedFilesPath.forEach(element => {
                if (element in store.addingList.value) {
                    delete store.addingList.value[element]
                }
            });
        }
    } catch (error) {
        error.value = error
    }
}
</script>