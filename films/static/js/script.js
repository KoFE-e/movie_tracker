window.addEventListener('DOMContentLoaded', () => {

    // Pagination

    function disableAllActiveElements(numPages, activeClass) {
        numPages.forEach(item => {
            item.classList.remove(activeClass);
        });
    }

    function showPage(pageItems, pageNum, pages) {
        disableAllActiveElements(pageItems, 'active');
        pageItems[pageNum].classList.add('active');

        disableAllActiveElements(pages, 'search_cards_page_active');
        pages[pageNum - 1].classList.add('search_cards_page_active');
    }

    function updateCounters(beginNum, endNum, cards, begin, end) {
        beginNum = pageNum * 6 + 1 - 6;
        endNum = pageNum * 6;
        if (endNum > cards.length) {
            endNum = cards.length;
        }
        begin.textContent = beginNum;
        end.textContent = endNum;
    }

    const pages = document.querySelectorAll('.search_cards_page'),
          cards = document.querySelectorAll('.card'),
          navlinkNums = document.querySelector('.pagination'),
          numPages = document.querySelectorAll('.num_page'),
          pageItems = document.querySelectorAll('.page-item'),
          prevArrow = document.querySelector('.prev-arrow'),
          nextArrow = document.querySelector('.next-arrow');

    const begin = document.querySelector('.search_cards_page_begin'),
          end = document.querySelector('.search_cards_page_end'),
          total = document.querySelector('.search_cards_total');

    total.textContent = cards.length;
    let beginNum = 1, endNum = 6;
    begin.textContent = beginNum;
    if (cards.length < 6) {
        endNum = cards.length;
    }
    end.textContent = endNum;
    
    let pageNum = 1;

    pages[0].classList.add('search_cards_page_active');
    pageItems[1].classList.add('active');

    navlinkNums.addEventListener('click', (e) => {
        e.preventDefault();
        console.log(e.target);
        numPages.forEach((item, i) => {
            if (e.target == item) {
                pageNum = i + 1;
                showPage(pageItems, pageNum, pages);
                updateCounters(beginNum, endNum, cards, begin, end);
            }
        });

        if (e.target == nextArrow) {
            pageNum += 1;
            if (pageNum > pages.length) {
                pageNum = 1;
            }
            showPage(pageItems, pageNum, pages);
            updateCounters(beginNum, endNum, cards, begin, end);
        }
        if (e.target == prevArrow) {
            pageNum -= 1;
            if (pageNum <= 0) {
                pageNum = pages.length;
            }
            showPage(pageItems, pageNum, pages);
            updateCounters(beginNum, endNum, cards, begin, end);
        }
        console.log(pageNum);
    })
});