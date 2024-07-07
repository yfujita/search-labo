<script>
import { defineComponent, reactive, onMounted } from "vue";

import SearchEvent from '@/events/SearchEvent';
import FormEvent from '@/events/FormEvent';

/**
 * Component for search form.
 */
export default defineComponent({

  props: {
  },

  setup(props, context) {
    // reactive data
    const state = reactive({
      query: '',
      searchType: 'basic',
    });

    onMounted(() => {
      // Handle updates to form value by other components.
      FormEvent.onUpdateFormValue((data) => {
        state.query = data;
      });
    });

    // method definitions

    /**
     * Submit the form.
     * If resultPage is empty, search on the current page.
     */
    const submit = (event) => {
      // Process on current page if resultPage is empty.
      const searchCond = SearchEvent.getInitialSearchCond();
      if (state.query !== '') {
        searchCond.q = state.query;
      }
      console.log('searchType: ' + state.searchType);
      searchCond.searchType = state.searchType;
      // Emit search event.
      SearchEvent.emitBasicSearch(searchCond);
      event.preventDefault();
      return;
    };

    return {
      state,
      submit,
    };
  },
});
</script>


<template>
  <form action="" method="GET" class="searchLaboForm" styleId="searchForm" @submit="submit">
    <div class="row mb-3">
      <label for="contentQuery" class="form-label col-2 col-form-label">Query</label>
      <div class="col-5">
        <input id="contentQuery" v-model="state.query" type="text" name="searchLabo.query" maxlength="1000" size="50" class="query form-control" autocomplete="off">
      </div>
    </div>
    <div class="row mb-3">
      <label for="exampleInputEmail1" class="form-label col-2 col-form-label">Search Type</label>
      <div class="col-5">
        <select v-model="state.searchType" id="queryType" class="form-select" aria-label="">
          <option value="basic">Basic</option>
          <option value="knn">kNN</option>
        </select>
      </div>
    </div>
    <div class="row mb-3">
      <div class="col-3">
        <button type="submit" name="search" class="searchButton btn btn-primary">
          Search
        </button>
      </div>
    </div>
  </form>
</template>
