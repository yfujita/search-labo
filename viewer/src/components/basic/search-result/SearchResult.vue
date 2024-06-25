<script>
import { defineComponent, reactive, onMounted, nextTick } from "vue";

import FrontHelper from "@/helper/FrontHelper";
import SearchResultHelper from "@/helper/SearchResultHelper";
import SearchService from "@/service/SearchService";

import SearchEvent from "@/events/SearchEvent";
import ResultHeader from "@/components/basic/search-result/ResultHeader";
import ResultItem from "@/components/basic/search-result/ResultItem";
import ResultPagination from "@/components/basic/search-result/ResultPagination";

const { getUrlParameters } = FrontHelper();
const searchResultHelper = SearchResultHelper();


/**
 * Component for search result.
 */
export default defineComponent({
  components: {
    "result-header": ResultHeader,
    "result-item": ResultItem,
    "result-pagination": ResultPagination,
  },
  props: {
    // Url of fess.
    esUrl: {
      type: String,
      default: "http://localhost:19200/",
    },
    // Page size of search result..
    pageSize: {
      type: Number,
      default: 10,
    },
  },

  setup(props, context) {
    // reactive data
    const state = reactive({
      show: false,
      searching: false,
      recordCount: -1,
      recordCountRelation: "EQUAL_TO",
      startRecordNumber: -1,
      endRecordNumber: -1,
      execTime: -1,
      q: "",
      hits: [],
      pageInfo: {
        pageNumbers: [],
        currentPageNumber: -1,
        prevPage: false,
        nextPage: false,
      },
      searchCond: {},
    });

    const searchService = new SearchService(props.esUrl);

    onMounted(() => {
      console.log("Init search result.");
      // Handle search event.
      SearchEvent.onBasicSearch((searchCond) => {
        search(searchCond);
      });
    });

    nextTick(() => {
      const urlParams = getUrlParameters();
    });

    // method definitions
    const search = (searchCond) => {
      // Copy search condition for custormization.
      const copiedSearchCond = SearchEvent.copySearchCond(searchCond);
      copiedSearchCond.pageSize = props.pageSize;
      searchService.search(copiedSearchCond).then ((response) => {
        _updateSearchState(response, copiedSearchCond);
        state.show = true;
        if (searchCond.addition.scrollTop) {
          _scrollToTop();
        }
      }).catch((error) => {
        console.error("Failed to search.", error);
      });
    };

    const _updateSearchState = (response, searchCond) => {
      console.log('update search state.');
      state.recordCount = response.hits.total.value;
      state.recordCountRelation = response.hits.total.relation;
      state.startRecordNumber = (searchCond.page - 1) * searchCond.pageSize + 1;
      state.endRecordNumber = state.startRecordNumber + response.hits.hits.length - 1;
      state.execTime = response.took;
      state.q = searchCond.q;
      state.hits = response.hits.hits;
      state.pageInfo = searchResultHelper.getPageInfo(response.hits.total.value, searchCond.page, searchCond.pageSize);
      state.searchCond = searchCond;

      console.log("Updated state:", state);
    };

    const _scrollToTop = () => {
      const boxEle = document.querySelector("#search-result-box");
      const top = boxEle.getBoundingClientRect().top + window.pageYOffset;
      window.scrollTo({
        top: top,
        behavior: "instant",
      });
    };

    return {
      state,
      search
    };
  },

});
</script>

<template>
  <div id="search-result-box" style="position: relative">
    <template v-if="state.show">
      <result-header
        :record-count-relation="state.recordCountRelation"
        :record-count="state.recordCount"
        :start-record-number="state.startRecordNumber"
        :end-record-number="state.endRecordNumber"
        :exec-time="state.execTime"
        :current-search-cond="state.searchCond"
      />
      <div id="result" class="">
        <ol class="list-unstyled">
          <li v-for="(hit) in state.hits" :key="hit._id">
            <result-item
              :search-hit="hit"
            />
          </li>
        </ol>
      </div>
      <div>
        <nav id="subfooter" class="mx-auto">
          <result-pagination
            v-if="state.recordCount > 0"
            :page-numbers="state.pageInfo.pageNumbers"
            :current-page-number="state.pageInfo.currentPageNumber"
            :prev-page="state.pageInfo.prevPage"
            :next-page="state.pageInfo.nextPage"
            :current-search-cond="state.searchCond"
          />
        </nav>
      </div>
      <div v-if="state.searching" class="search-waiting" />
    </template>
  </div>
</template>
