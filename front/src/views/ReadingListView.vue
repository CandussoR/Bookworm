<template>
    <div class="flex flex-col m-auto" v-if="readingList">
        <h1 class="text-5xl text-center my-10">
            {{ readingList.name }}
        </h1>

        <div id="list-description" class="bg-base-200 ">
            <p class="text-center my-5" v-if="readingList.description">{{ readingList.description }}</p>
        </div>

        <p class="text-center my-10">Books read : {{booksRead }} / {{ readingList.reading_list.length }}</p>

        <ul class="text-center max-w-xl">
            <li v-for="(item,i) in readingList.reading_list" :key="item.ebook_guid">
                <div class="flex items-center">
                    <div class="mr-6">
                        <input name="read" type="checkbox" @click="toggleRead(i)">
                    </div>
                    <div class="mr-6">
                        <p :class="item.read ? 'line-through text-gray-600' : ''"><b>{{ item.ebook_name }}</b></p>
                        <p class="ml-10">{{item.comment}}</p>
                    </div>
                    <div>
                        <img class="cursor-pointer" src="@/assets/delete.svg" alt="Delete" @click="deleteItem(i, item.ebook_guid)">
                    </div>
                </div>
            </li>
        </ul>
    </div>
    <div v-else>
        <p>Loading...</p>
    </div>
</template>

<script setup>
import { useReadingListStore } from '@/stores/readingLists';
import { onMounted, ref, computed} from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const store = useReadingListStore()
const readingList = ref(null)
const readingListIndex = ref(null)
const booksRead = computed(() => readingList.value.reading_list.map(item => item.read).reduce((acc,curr) => acc+curr, 0))
const dirty = ref(0)
const modified = ref({})

onMounted(async () => {
    if (!store.readingLists) {
        await store.index();
    }

    for (let i = 0; i < store.readingLists.length ; i++) {
        if (!(store.readingLists[i].reading_list_guid === route.params.guid)) continue;
        // Ugly af deep copy
        readingList.value = JSON.parse(JSON.stringify(store.readingLists[i]));
        readingListIndex.value = i;
    }
})

function toggleRead(i) {
    if (readingList.value.reading_list[i].read === 1) {
        readingList.value.reading_list[i].read = 0
    } else {
        readingList.value.reading_list[i].read = 1
    }
    dirty.value = 1
    updateModify("read", readingList.value.reading_list[i].read, i, "update")
    
}

function deleteItem(index) {
    updateModify(null, null, index, "delete")
}

function updateModify(key=null, value=null, index=null, action=null) {
    if (index && (!action || !["update", "delete"].includes(action))) {
        throw new Error("If there's an index, there's an action.")
    }

    if (isOriginalValue(key, value, index, action)) {
        deleteFromModified(key, value, index, action)
        return;
    } else if (hasBeenModified(key, value, index, action)) {
        deleteFromModified(key, value, index, action);
    }

    if (index === null && value && key) {
        modified.value[key] = value;
        return;
    }

    if (!("items" in modified.value)) {
        modified.value.items = []
    }

    if (action === "update") {
        modified.value.items.push({ "i": index, "action": action, [key]: value });
        return;
    } else if (action === "delete") {
        modified.value.items.push({ "i": index, "action": "delete" })
        readingList.value.reading_list.splice(index, 1);
        return;
    }
}

function isOriginalValue(key, value, index=null, action=null) {
    if (action == "delete") {
        return false;
    }

    const storeReadingList = store.readingLists[readingListIndex.value]
    if (index !== null && action) {
        return storeReadingList.reading_list[index][key] === value;
    }

    if (storeReadingList[key] === value) return true;
    else return false;
}

function hasBeenModified(key, value, index=null, action=null) {
    // Not checking for delete for now since you can't update something you actually deleted
    if (index !== null && action) {
        if (!(modified.value.items) || !modified.value.items.length) return false;

        for (let i =0; i < modified.value.items.length; i++) {
            if (modified.value.items[i]["i"] === index && [key] in modified.value.items[i]) return true;
        }
    } 
    if ([key] in modified.value) {
        return true;
    }
    return false
}


function deleteFromModified(key, value, index=null, action=null) {
    // If we're here, either we returned to an original value or we found that value has been modified before and we're cleaning
    if (index !== null && action == "update") {

        for (let i=0; i < modified.value.items.length; i++) {
            if (modified.value.items[i]["i"] === index && key in modified.value.items[i]) {
                modified.value.items.splice(i,1);
                return;
            }
        }

    } else if (index !== null && action == "delete") {

        modified.value.items = modified.value.items.filter(el => el.i === index)

    } else {

        delete modified.value.key

    }
}
</script>

<style scoped></style>