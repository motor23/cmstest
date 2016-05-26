import {expect, assert} from 'chai';
import paginate from '../../src/js/util/paginate';


describe('paginate', function () {
    it('in the middle', function () {
        const pages = paginate(100, 1, 50, 2, 3);
        expect(pages).to.eql([1, 2, null, 47, 48, 49, 50, 51, 52, 53, null, 99, 100]);
    });

    it('in the start', function () {
        const pages = paginate(100, 1, 1, 2, 3);
        expect(pages).to.eql([1, 2, 3, 4, null, 99, 100]);
    });

    it('neare the start', function () {
        const pages = paginate(100, 1, 5, 2, 3);
        expect(pages).to.eql([1, 2, 3, 4, 5, 6, 7, 8, null, 99, 100]);
    });

    it('outside the range', function () {
        const pages = paginate(100, 1, 200, 2, 3);
        expect(pages).to.eql([1, 2, null, 99, 100]);
    });

    it('near the end', function () {
        const pages = paginate(100, 1, 99, 2, 5);
        expect(pages).to.eql([1, 2, null, 94, 95, 96, 97, 98, 99, 100]);
    });

    it('one range inside another', function () {
        const pages = paginate(100, 1, 4, 8, 2);
        expect(pages).to.eql([1, 2, 3, 4, 5, 6, 7, 8, null, 93, 94, 95, 96, 97, 98, 99, 100]);
    });

    it('shor range', function () {
        const pages = paginate(2, 1, 99, 2, 5);
        expect(pages).to.eql([1, 2]);
    });

    it('test case 1', function () {
        const pages = paginate(610, 10, 10, 3, 5);
        expect(pages).to.eql([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, null, 59, 60, 61]);
    });

    it('test case 2', function () {
        const pages = paginate(610, 10, 12, 3, 5);
        expect(pages).to.eql([1, 2, 3, null, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, null, 59, 60, 61]);
    });

    it('test case 3', function () {
        const pages = paginate(610, 10, 22, 3, 5);
        expect(pages).to.eql([1, 2, 3, null, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, null, 59, 60, 61] );
    });

    it('test case 4', function () {
        const pages = paginate(610, 10, 50, 3, 5);
        expect(pages).to.eql([1, 2, 3, null, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, null, 59, 60, 61]);
    });

    it('test case 5', function () {
        const pages = paginate(610, 10, 55, 3, 5);
        expect(pages).to.eql([1, 2, 3, null, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]);
    });
});