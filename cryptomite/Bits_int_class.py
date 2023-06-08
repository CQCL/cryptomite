from random import randint

class BitsAsInt:
    def __init__(self, input):
        self.bitstring = 0 # type int
        if type(input) == list:
            for x in input:
                self.bitstring <<= 1
                self.bitstring ^= int(x)
            self.length = len(input)
        elif type(input) == int:
            self.bitstring = input
            self.length = len(bin(input)) - 2
        elif input == None:
            self.length = 0
        # except we need type bytes, not int
        
    def __eq__(self, other):
        is_equal = (self.bitstring == other.bitstring) and (self.length == other.length)
        return is_equal
        
    def __index__(self):
        return self.bitstring
        
    def __bool__(self):
        return bool(self.length)
                
    def __len__(self):
        return self.length
                
    def __str__(self):
        if self.length == 0:
            return '0b[Empty]'
        bin_str = bin(self.bitstring)[2:]
        padding = '0' * (self.length - len(bin_str)) # ensures preceeding 0s are printed
        return '0b' + padding + bin_str
        
    def __add__(self, other):
        added_int = (self.bitstring << len(other)) ^ other.bitstring
        added_bits = BitsAsInt(added_int)
        added_bits.length = len(self) + len(other)
        return added_bits
    
    def set_item_index(self, in_i):
        i = in_i
        if i < 0:
            i += len(self)
        if i < 0 or i >= len(self):
            raise IndexError("BitsAsInt index out of range")
        return i
    
    def set_slice_indices(self, in_start, in_stop, in_step):
        for x in [in_start, in_stop, in_step]:
            if x != None and type(x) != int:
                raise TypeError("slice indices must be integers or None or have an __index__ method")
                return
        step = in_step if in_step != None else 1
        if step == 0:
            raise ValueError("slice step cannot be zero")
            return
        if in_start != None:
            i = in_start % len(self) if (-len(self) <= in_start < len(self)) else in_start
            i = max(0, i) #if step > 0 else max(-1, i)?
            i = min(len(self), i) if step > 0 else min(len(self) - 1, i)
        else:
            i = 0 if step > 0 else len(self) - 1
        if in_stop != None:
            j = in_stop % len(self) if (-len(self) <= in_stop < len(self)) else in_stop
            j = max(-1, j)
            j = min(len(self), j)
        else:
            j = len(self) if step > 0 else -1
        return i, j, step
    
    def __getitem__(self, key):
        if isinstance(key, int):
            i = self.set_item_index(key)
            right_shift = len(self) - i - 1
            return (self.bitstring >> right_shift) & 1
        elif isinstance(key, slice):
            i, j, step = self.set_slice_indices(key.start, key.stop, key.step)
            as_int = 0
            ret_len = 0
            for n in range(i, j, step):
                as_int <<= 1
                as_int ^= self[n]
                ret_len += 1
            ret_bits = BitsAsInt(as_int)
            ret_bits.length = ret_len
            return ret_bits
        else:
            raise TypeError(f"list indices must be integers or slices, not {type(key)}")
        return
            
    def __setitem__(self, key, new):
        if isinstance(key, int):
            if type(new) != int or (new not in [0,1]):
                raise TypeError("can only assign one bit")
            i = self.set_item_index(key)
            left_shift = self.length - i - 1
            bitmask = 1 << left_shift # align with start
            if new == 1: # if 1 set to 1
                self.bitstring |= bitmask
            else: # if 0 set to 0
                self.bitstring &= ~bitmask
            return
        elif isinstance(key, slice): # if len(new) is smaller, it deletes things
            if type(new) != BitsAsInt:
                raise TypeError("can only assign BitsAsInt")
            i, j, step = self.set_slice_indices(key.start, key.stop, key.step)
            if len(new) != len(self[key]) and step != 1:
                raise ValueError(f"attempt to assign sequence of size {len(new)} to extended slice of size {len(self[key])}")
            if step == 1:
                newObj = self[:i] + new + self[j:]
                self.__dict__.update(newObj.__dict__)
            else: # only happens when len(new) == len(slice)
                k = 0
                for n in range(i, j, step):
                    self[n] = new[k]
                    k += 1
        else:
            raise TypeError(f"list indices must be integers or slices, not {type(key)}")
        return
        
    def copy(self):
        copied_bits = BitsAsInt(self.bitstring)
        copied_bits.length = self.length
        return copied_bits
        
    def append(self, i):
        if i in [0,1]:
            self.length += 1
            self.bitstring <<= 1
            self.bitstring += i
        else:
            raise TypeError("can only append 0 or 1")
        return
        
    def pop(self):
        if self.length > 0:
            b = self.bitstring & 1
            self.bitstring >>= 1
            self.length -= 1
            return b
        else:
            raise IndexError("pop from empty list")
        return
        
    def count(self, b):
        if b not in [0,1]:
            raise ValueError("only bits can be counted")
            return
        sum = 0
        for i in range(self.length):
            sum += self[i]
        if b == 1:
            return sum
        return self.length - sum # number of 0s






