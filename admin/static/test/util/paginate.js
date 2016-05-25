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
});