<template>
    <main class="w-full overflow-hidden">

        <h1 class="text-5xl text-center my-10">Dragged books</h1>
        <h2 class="text-2xl text-center my-5">Waiting for review</h2>

        <EditableMetadataTable @updated="store.updateAddingList($event)"/>

    </main>
</template>

<script setup>
import EditableMetadataTable from '@/components/EditableMetadataTable.vue';
import { useAddingListStore } from '@/stores/addingList';
const store = useAddingListStore()
</script>

<style>

</style>