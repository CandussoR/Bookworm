<template>
    <main class="w-full overflow-hidden">

        <h1 class="text-5xl text-center my-10">Dragged books</h1>
        <h2 class="text-2xl text-center my-5">Waiting for review</h2>

        <EditableMetadataTable :ebooks="addingListStore.addingList" @change="editStoreList"/>

    </main>
</template>

<script setup>
import EditableMetadataTable from '@/components/EditableMetadataTable.vue';
import { useAddingListStore } from '@/stores/addingList';
import { onMounted } from 'vue';

const addingListStore = useAddingListStore()

onMounted(async () => {
    if (!addingListStore.addingList) {
        await addingListStore.getAddingList()
    }
})

async function editStoreList(event) {
    console.log(event);
}
</script>

<style>

</style>