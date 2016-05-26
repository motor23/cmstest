export default function paginate(total, limit, page, edge=3, surround=5) {
    const totalPages = Math.ceil(total / limit);
    const currentPage = page;
    const leftEnd = Math.min(edge, totalPages);
    const surroundStart = Math.min(Math.max(1, currentPage - surround), totalPages + 1);
    const surroundEnd = Math.min(currentPage + surround, totalPages);
    const rightStart = Math.min(Math.max(1, totalPages -  edge + 1), totalPages + 1);
    let ranges = [];
    ranges.push([1, leftEnd + 1]);
    if (surroundEnd >= surroundStart) {
        ranges.push([surroundStart, surroundEnd + 1]);
    }
    if (totalPages >= rightStart) {
        ranges.push([rightStart, totalPages + 1]);
    }
    ranges.sort(([a1, a2], [b1, b2]) => {
        if (a1 > b1) return 1;
        if (a1 < b1) return -1;
        if (b1 > b2) return 1;
        if (b1 < b2) return -1;
        return 0;
    });
    let pages = [];
    for (let i = ranges[0][0]; i < ranges[0][1]; i++) {
        pages.push(i);
    }
    for (let i = 1; i < ranges.length; i++) {
        const last = pages[pages.length - 1];
        const start = ranges[i][0];
        const end = ranges[i][1];
        if (end <= last) {
            continue;
        }
        if (start <= last + 2) {
            for (let j = last + 1; j < end; j++) {
                pages.push(j);
            }
        }
        else {
            pages.push(null);
            for (let j = start; j < end; j++) {
                pages.push(j);
            }
        }
    }
    return pages;
}