import axios from 'axios';
import Mustache from 'mustache';

import searchTemplateBasic from '@/assets/search-template/basic.mustache';


/**
 * SearchService.js
 * 
 * This module provides search functions.
 */
export default class {
  constructor(esUrl){
    this.esUrl = esUrl.endsWith('/') ? esUrl.substring(0, esUrl.length - 1): esUrl;
  }
  
  /**
   * Get fess version.
   * @returns fessVersion
   */
  getFessVersion() {
    const url = this.esUrl + '/json';
    return new Promise((resolve, reject) =>  {
      try {
        axios.get(
          url
        ).then((res) => {
          const version = res.data.response.version;
          resolve(version);
        }).catch((e) => {
          console.log('ERROR!!');
          reject(e);
        });
      } catch (e) {
        console.log('ERROR!!!');
        reject(e);
      }
    });
  }

  /**
   * Search
   * @param {Object} searchCond 
   * @param {Object} state Update by search result.
   * @returns Promise<SearchResponse>
   */
  search(index, searchCond) {
    return new Promise((resolve, reject) =>  {
      const url = `${this.esUrl}/${index}/_search`;
      const searchParams = this._buildParams(searchCond);
      const query = this._renderQuery(searchParams);

      console.log('Search cond...', searchCond);
      console.log('Search start...', query);
  
      axios.post(
        url,
        query,
        {
          headers: {
            'Content-Type': 'application/json',
          }
        }
      ).then((response) => {
        console.log('Search success!', response.data);
        try {
          resolve(response.data);
        } catch (e) {
          reject(e);
        }
      }).catch((res) => {
        console.log('ERROR!');
        reject(res);
      });
    });
  }

  /**
   * Build params
   */
  _buildParams(searchCond) {
    const searchParams = {
      keywords: searchCond.q.split(/[\u0020\u3000]+/),
      sort: searchCond.sort,
      from: (searchCond.page - 1) * searchCond.pageSize,
      size: searchCond.pageSize,
    };
    return searchParams;
  }


  /**
   * Render query
   */
  _renderQuery(searchParams) {
    const rendered = Mustache.render(searchTemplateBasic, searchParams);
    return rendered.replace(/,(?=\s*[}\]])/g, '');
  }
}