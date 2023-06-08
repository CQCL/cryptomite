import unittest
from Bits_int_class import BitsAsInt
from random import randint, getrandbits

def create_random_instance(n: int) -> [list[bool], BitsAsInt]:
    #print("Generating test bits")
    test_bool_list = []
    for i in range(n):
        b = randint(0,1)
        test_bool_list.append(bool(b))
    test_bits = BitsAsInt(test_bool_list)
    return [test_bool_list, test_bits]
    
size = 10

size1 = 10
size2 = 20

class TestBitsAsIntClass(unittest.TestCase):

    def test_bool_list_init(self):
        print("  Testing initialising from bool list")
        [test_bool, test_bits] = create_random_instance(size)
        self.assertEqual(len(test_bool), len(test_bits))
        self.assertEqual(len([]), len(BitsAsInt([])))
        
    def test_int_init(self):
        n_tests = 100
        print("  Testing initialising from", n_tests, "ints")
        for t in range(n_tests):
            x = getrandbits(size)
            test_bits = BitsAsInt(x)
            for i in range(len(bin(x))-3, -1, -1):
                self.assertEqual(test_bits[i], x&1)
                x >>= 1

    # TESTS for __add__
        
    def test_add_empty(self):
        print("  Testing adding empty BitsAsInt")
        empty = BitsAsInt(None)
        [test_bool, test_bits] = create_random_instance(size)
        self.assertEqual(empty, empty + empty)
        self.assertEqual(test_bits, test_bits + empty)
        self.assertEqual(test_bits, empty + test_bits)
    
    def test_add_different_sizes(self):
        print("  Testing adding BitsAsInt")
        [bool1, bits1] = create_random_instance(size1)
        [bool2, bits2] = create_random_instance(size2)
        self.assertEqual(BitsAsInt(bool1 + bool2), bits1 + bits2)
        self.assertEqual(BitsAsInt(bool2 + bool1), bits2 + bits1)

    # TESTS for __getitem__ with index

    def test_valid_indices(self):
        print("  Testing example[i] where 0 <= i < len(example)")
        [test_bool, test_bits] = create_random_instance(size)
        for i in range(size):
            self.assertEqual(int(test_bool[i]), test_bits[i])
            
    def test_wraparound_index(self):
        print("  Testing wraparound index")
        [test_bool, test_bits] = create_random_instance(size)
        for i in range(-1, -size - 1, -1):
            self.assertEqual(int(test_bool[i]), test_bits[i])
            
    def test_out_of_bounds_index(self):
        print("  Testing out of bounds index")
        [test_bool, test_bits] = create_random_instance(size)
        for i in [-size-1, size]:
            with self.assertRaises(IndexError) as exception_context:
                test_bits[i]
            self.assertEqual(str(exception_context.exception), "BitsAsInt index out of range")
            
    # TESTS fpr __setitem__ with index
    
    def test_set_index(self):
        [test_bool, test_bits] = create_random_instance(size)
        print("  Testing set index")
        for i in range(size):
            b = randint(0,1)
            test_bits[i] = b
            test_bool[i] = bool(b)
            for j in range(size):
                self.assertEqual(bool(test_bits[j]), test_bool[j]) # checks that only the changed value has changed
            
    # TESTS for __getitem__ with slice
    
    def test_out_step_zero(self):
        print("  Testing slice where step = 0")
        [test_bool, test_bits] = create_random_instance(size)
        with self.assertRaises(ValueError) as exception_context:
            test_bits[0:size-1:0]
        self.assertEqual(str(exception_context.exception), "slice step cannot be zero")
            
    def test_slice_indices_not_int(self):
        print("  Testing non-int slice")
        [test_bool, test_bits] = create_random_instance(size)
        for [i,j,step] in [[0,size-1,"a"],[0,2.2,1],[True,size-1,1]]:
            with self.assertRaises(TypeError) as exception_context:
                test_bits[i:j:step]
            self.assertEqual(str(exception_context.exception), "slice indices must be integers or None or have an __index__ method")
            
    def test_slice_defaults(self):
        print("  Testing slice defaults example[::]")
        [test_bool, test_bits] = create_random_instance(size)
        self.assertEqual(test_bits[::], test_bits)
        
    def test_less_than_min_slice(self):
        print("  Testing example[i] where i < -len(example)")
        [test_bool, test_bits] = create_random_instance(size)
        i = -size - 1
        self.assertEqual(test_bits[i:], test_bits[0:])
    
    def test_greater_than_max_slice(self):
        print("  Testing example[i] where i > len(example)")
        [test_bool, test_bits] = create_random_instance(size)
        j = size + 1
        self.assertEqual(test_bits[:j], test_bits[:size])
        
    def test_random_slices(self):
        n_tests = 100
        print("  Testing", n_tests, "random slices")
        [test_bool, test_bits] = create_random_instance(size)
        for t in range(n_tests):
            i = randint(-size, 2*size)
            j = randint(-size, 2*size)
            step = randint(-size, 2*size)
            while step == 0:
                step = randint(-size, 2*size)
            sliced_bool = test_bool[i:j:step]
            sliced_bits = test_bits[i:j:step]
            self.assertEqual(len(sliced_bool), len(sliced_bits))
            for k in range(len(sliced_bool)):
                self.assertEqual(int(sliced_bool[k]), sliced_bits[k])
                
    # TEST for __setitem__ with slice
                
    def test_set_slice_step_1(self):
        print("  Testing simple slice setting (step = 1)")
        [test_bool, test_bits] = create_random_instance(size)
        n_tests = 1
        for t in range(n_tests):
            i = randint(0, size - 1)
            j = randint(i+1, size)
            n_size = j - i
            [new_bool, new_bits] = create_random_instance(n_size)
            test_bool[i:j] = new_bool
            test_bits[i:j] = new_bits
            for k in range(size):
                self.assertEqual(int(test_bool[k]), test_bits[k])
                
    def test_slice_with_other_steps(self):
        print("  Testing slice setting with other steps")
        [test_bool, test_bits] = create_random_instance(size)
        for step in [-2,-1,2]:
            slice_size = len(test_bits[::step])
            [new_bool, new_bits] = create_random_instance(slice_size)
            test_bool[::step] = new_bool
            test_bits[::step] = new_bits
            for k in range(size):
                self.assertEqual(int(test_bool[k]), test_bits[k])
            
    def test_set_slice_bad_size(self):
        print("  Testing slice setting when len(new_bits) != slice_size and step != 1")
        [test_bool, test_bits] = create_random_instance(size)
        for [i,j,step] in [[size-1, 0, -2], [0,size,3]]:
            slice_size = len(test_bits[i:j:step])
            for new_size in [slice_size + 1, slice_size - 1]:
                [new_bool, new_bits] = create_random_instance(new_size)
                with self.assertRaises(ValueError) as exception_context:
                    test_bool[i:j:step] = new_bool
                arr_error = str(exception_context.exception)
                with self.assertRaises(ValueError) as exception_context:
                    test_bits[i:j:step] = new_bits
                bits_error = str(exception_context.exception)
                self.assertEqual(arr_error, bits_error)
    
    # TEST other methods
    
    def test_copy(self):
        print("  Testing .copy()")
        [test_bool, test_bits] = create_random_instance(size)
        c = test_bits.copy()
        self.assertEqual(c, test_bits)
        
    def test_append(self):
        print("  Testing .append() with bit")
        [test_bool, test_bits] = create_random_instance(size)
        for b in [0,1]:
            test_bits.append(b)
            if b:
                test_bool.append(True)
            else:
                test_bool.append(False)
            self.assertEqual(len(test_bool), len(test_bits))
            for k in range(len(test_bits)):
                self.assertEqual(int(test_bool[k]), test_bits[k])
                
    def test_pop(self):
        print("  Testing .pop()")
        [test_bool, test_bits] = create_random_instance(size)
        while test_bits:
            b = test_bits.pop()
            b_bool = test_bool.pop()
            self.assertEqual(int(b_bool), b)
            self.assertEqual(len(test_bool), len(test_bits))
        
    def test_empty_pop(self):
        print("  Testing .pop() on empty BitsAsInt")
        empty_bits = BitsAsInt(None)
        with self.assertRaises(IndexError) as exception_context:
            empty_bits.pop()
        bits_error = str(exception_context.exception)
        self.assertEqual("pop from empty list", bits_error)
           
    def test_count(self):
        n_tests = 100
        print("  Testing count on", n_tests, "random BitsAsInt objects")
        for t in range(n_tests):
            [test_bool, test_bits] = create_random_instance(size)
            for [bool_val, b] in [[True, 1], [False, 0]]:
                count_bool = test_bool.count(bool_val)
                count_b = test_bits.count(b)
                self.assertEqual(count_bool, count_b)
    
if __name__ == '__main__':
    print(f"Testing with size {size}:")
    unittest.main()

