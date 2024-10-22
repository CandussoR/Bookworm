<template>
    <div class="flex flex-col m-auto" v-if="readingList">

        <h1 id="reading-list-name" class="text-5xl text-center my-10">
            {{ readingList.name }}
        </h1>

        <!-- Description -->
        <div v-if="!editDescription" id="list-description" class="flex justify-evenly bg-base-200 container">
            <p v-if="readingList.description" class="text-center p-5" >{{ readingList.description }}</p>
            <p v-else class="italic my-5">Add a description</p>
            <img class="cursor-pointer" src="@/assets/edit.svg" alt="edit-description"
                @click="editDescription = !editDescription">
        </div>
        <div v-else id="list-description" class="flex justify-evenly bg-base-200 container">
            <input id="list-edit" class="bg-inherit input input-ghost w-full max-w-xs text-sm" 
                name="list-edit" v-model="newDescription" required>
            <img class="cursor-pointer" src="@/assets/check.svg" alt="validate-description"
                @click="updateDescription()">
            <img class="cursor-pointer" src="@/assets/close.svg" alt="cancel-description"
                @click="editDescription = !editDescription">
            {{newDescription}}
        </div>

        <!-- Books read -->
        <p id="books-read" class="text-center my-10">Books read : {{booksRead }} / {{ readingList.items.length }}</p>

        <!-- Reading List -->
        <ul id="reading-list" class="max-w-xl">
            <!-- Item -->
            <li v-for="(ebook,i) in readingList.items" :key="ebook.ebook_guid">
                <div :id="'item-' + i + '-row'" class="flex items-center mb-4">
                    <!-- Read -->
                    <div :id="'item-' + i + '-read-icon-div'" class="mr-6 cursor-pointer" @click="toggleRead(i)">
                        <ReadSvg :read="ebook.read" />
                    </div>

                    <!-- Details -->
                    <div :id="'item-' + i + '-details'" class="mr-6">
                        <!-- Book title -->
                        <p :id="'item-' + i + '-title'" class="text-center mb-2"
                            :class="{'line-through text-gray-600' : ebook.read }"><b>{{ ebook.title }}</b></p>
                        <!-- Comment about book -->
                        <input class="bg-inherit input-ghost w-full max-w-xs ml-10 text-sm"  :id="'item-' + i + '-comment'"
                            type="text" required @keyup.enter="(event) => updateBookComment(i, event)"
                            :value="ebook.comment" placeholder="Add a comment..."
                            >
                    </div>

                    <!-- CTA -->
                    <div :id="'cta-' + i">
                        <img class="cursor-pointer" src="@/assets/delete.svg" alt="Delete"
                            @click="deleteItem(i, ebook.ebook_guid)">
                    </div>
                </div>
            </li>
        </ul>

        <!-- Button && modal to add book -->
        <button id="add-book" class="btn btn-outline btn-neutral min-w-xl" @click="addBookModal.showModal()">
            Add a book
        </button>

        <dialog id="openAddBook" ref="addBookModal" class="modal" @keyup.esc="closeModal">
            <div class="modal-box">
                <h3 class="text-lg font-bold">Add a book</h3>
                <p class="py-4 text-xs">Press <kbd>Esc</kbd> key or click the button below to close</p>
                <div class="modal-action">
                    <form @submit.prevent="addBooksToModified" method="dialog">
                        <label for="ebooks">ebook : </label>
                        <input name="ebooks" type="text" list="ebookSearch" @input.stop="debounce">
                        <!-- if there is a button in form, it will close the modal -->
                        <button class="btn" type="submit">Add books</button>
                        <div id="searchResults">
                            <ul id="ebook-search-results" v-if="hasReceivedResponse && ebookSearchResult.length > 0">
                                <li class="hover:cursor-pointer hover:bg-base-100 my-2 px-6 py-1"
                                    v-for="ebook in ebookSearchResult" :key="ebook.ebook_guid"
                                    @click="addItem(ebook.ebook_guid)">
                                    {{ ebook.title }} ({{ ebook.author }})
                                </li>
                            </ul>
                            <p v-else-if="hasReceivedResponse && ebookSearchResult.length == 0">
                                No books related to this search.
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </dialog>
    </div>
    <div v-else>
        <p>Loading...</p>
    </div>

</template>

<script setup>
import { useReadingListStore } from '@/stores/readingLists';
import { onMounted, ref, computed, useTemplateRef} from 'vue';
import { useRoute } from 'vue-router';
import axios from '../utils/apiRequester';
import ReadSvg from '@/components/ReadSvg.vue';

const route = useRoute()
const store = useReadingListStore()
const changes = ref([])
const hasReceivedResponse = ref(0)
const readingList = ref(null)
const readingListIndex = ref(null)
const booksRead = computed(() => readingList.value.items.map(item => item.read).reduce((acc,curr) => acc+curr, 0) || 0)
const addBookModal = useTemplateRef('addBookModal');
const ebookSearchResult = ref([])
const timer = ref()
const newDescription = ref('')
const editDescription = ref(false)

onMounted(async () => {
    if (!store.readingLists) {
        await store.index();
    }

    for (let i = 0; i < store.readingLists.length ; i++) {
        if (!(store.readingLists[i].reading_list_guid === route.params.guid)) continue;
        // Ugly af deep copy
        readingList.value = JSON.parse(JSON.stringify(store.readingLists[i]));
        readingListIndex.value = i;
        if (readingList.value.description) {
            newDescription.value = readingList.value.description;
        }
    }
})


function toggleRead(i) {
    if (readingList.value.items[i].read === 1) {
        readingList.value.items[i].read = 0
    } else {
        readingList.value.items[i].read = 1
    }
    updateModify("read", readingList.value.items[i].read, i, "update")
}

function deleteItem(index) {
    updateModify(null, null, index, "delete")
}

function addItem(ebook_guid) {
    updateModify("ebook_guid", ebook_guid, null, "add")
}

async function updateBookComment(index, event) {
    hasReceivedResponse.value = 0;
    await updateModify("comment", event.target.value, index, "update")
    if (hasReceivedResponse.value) {
        event.currentTarget.blur();
    }
}

async function updateDescription() {
    hasReceivedResponse.value = 0;
    await updateModify("description", newDescription.value, null, "update")
    if (hasReceivedResponse.value) {
        editDescription.value = !editDescription.value
    }
}
/**
 * Procedure to determine how to bookkeep changes to a reading list.
 * @param {string} key - A key of a readingList object or of a list item
 * @param {string} value - The new value of specified key
 * @param {integer} index - Index of the modified item (works only with update and delete as actions)
 * @param {string} action - The type of action to execute on the reading list (add, update, delete)
 */
async function updateModify(key=null, value=null, index=null, action=null) {
    if (index && (!action || !["update", "delete"].includes(action))) {
        throw new Error("If there's an index, there's an action.")
    } else if (index !== null && index >= 0 && action && action !== "add") {
        throw new Error("If you add, you don't get to choose your index.")
    }

    let newValue = null
    const theKey = key === "name" || key === "description" ? key : "items"
    if (theKey === "items") {
        if (action === "add") {
            newValue = {"action" : action, "key" : key, "val" : value}
        } else if (action === "delete") {
            newValue = {"action" : action, "i": index}
        } else if (action === "update") {
            newValue = {"action" : action, "i" : index, "key" : key, "val" : value}
        }
        else {
            throw new Error("Wrong action man")
        }
    }

    const data = {"reading_list_guid" : readingList.value.reading_list_guid,
                  [theKey] : newValue || value
    }

    try {
        const res = await axios.put('reading_lists', data)
        if (res.status !== 200) {
            throw new Error(res.status, res.statusText)
        }

        if (theKey !== "items") {
            changes.value.push({ [theKey]: readingList.value[theKey] })
        } else {
            if (action === "add") {
                changes.value.push({ "action": "delete", index: -1 })
            } else if (action === "update") {
                changes.value.push({ "action": action, [key]: readingList.value.items[index][key] })
            } else {
                changes.value.push({ "action": "add", [key]: value })
            }
        }

        // Updating value of current reading list to the returned value if the request was successfull
        for (let i = 0; i < store.readingLists.length; i++) {
            if (!(store.readingLists[i].reading_list_guid === route.params.guid)) continue;
            store.readingLists[i] = res.data
            break;
        }

        readingList.value = res.data;
        hasReceivedResponse.value = 1;
    }
    catch (error) {
        console.error(error);
    }
}


function debounce(event) {
    // On each input, we delete the timer set to only send a request with the latest input
    if (timer.value) {
        clearTimeout(timer.value)
    }
    // We also want to reset the received_response since we have not yet make the request
    hasReceivedResponse.value = 0

    if (event.target.value == '') {
        ebookSearchResult.value = []
        return;
    }
    // searchForBooks only gets called when user stops typing for 500ms
    timer.value = setTimeout(() => searchForBooks(event.target.value), 500)
}


async function searchForBooks(search) {
    const res = await axios.get(`ebooks?search=${search}`)
    hasReceivedResponse.value = 1
    if (res.data) {
        ebookSearchResult.value = res.data
    }
}

</script>

<style scoped></style>