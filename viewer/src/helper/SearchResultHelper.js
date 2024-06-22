/**
 * FrontHelper.js
 * 
 * This module provides helper functions for front.
 */
export default function () {

  // Get Url Parameters
  // @returns {Object<string, string[]>}
  const getPageInfo = (total, currentPage, pageSize) => {
    const pageNumbers = [];
    const maxPage = Math.ceil(total / pageSize) + 1;
    for (let i = 1; i <= maxPage; i++) {
      if (currentPage - 5 < i && i < currentPage + 5) {
        pageNumbers.push(i);
      }
    }
    const prevPage = currentPage > 1;
    const nextPage = currentPage < maxPage;
    return {
      pageNumbers: pageNumbers,
      currentPageNumber: currentPage,
      prevPage: prevPage,
      nextPage: nextPage,
    };
  };

  return {
    getPageInfo,
  };
}