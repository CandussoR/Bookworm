<template>
    <div class="card card-compact bg-base-100 w-96 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">{{ props.relation }}</h2>
        <p>{{ props.name }}</p>
        <div v-if="props.related">
            <span>Related {{props.relation.toLowerCase() + 's'}}</span> : <p>{{ props.related.join(', ')}}</p>
        </div>
    </div>
</div>

</template>

<script setup>
const props = defineProps({
    relation : String,
    name : String,
    related : Array[String] || null
})
</script>