/*
 * reuse_buffer.hh
 *
 * Header file for the ReuseBuffer class used in the gem5 O3 CPU model.
 * The ReuseBuffer uses PC and operand values to check for instruction matches
 * and stores the result upon instruction completion, using FIFO replacement.
 */

#ifndef __REUSE_BUFFER_HH__
#define __REUSE_BUFFER_HH__

#include <vector>
#include <deque>
#include "base/types.hh"        // For types like Addr, RegVal
#include "base/pcstate.hh"      // For PCStateBase

// Define the size of the reuse buffer
#define REUSE_BUFFER_SIZE 128  // Adjust the size as needed

namespace gem5
{

namespace o3
{

class ReuseBuffer
{
  public:
    // Structure to hold an entry in the reuse buffer
    struct Entry {
        PCStateBase pc;
        std::vector<RegVal> operands;
        RegVal result;

        Entry(const PCStateBase &pc_state,
              const std::vector<RegVal> &ops,
              const RegVal &res)
            : pc(pc_state), operands(ops), result(res) {}
    };

    ReuseBuffer();
    ~ReuseBuffer();

    // Check if an instruction with the same PC and operands exists
    bool contains(const PCStateBase &pc,
                  const std::vector<RegVal> &operands) const;

    // Get the result of an instruction from the reuse buffer
    RegVal getResult(const PCStateBase &pc,
                     const std::vector<RegVal> &operands) const;

    // Insert a new instruction into the reuse buffer
    void insert(const PCStateBase &pc,
                const std::vector<RegVal> &operands,
                const RegVal &result);

  private:
    // The reuse buffer implemented as a deque for FIFO behavior
    std::deque<Entry> buffer;

    // Helper function to compare entries
    bool isMatch(const Entry &entry,
                 const PCStateBase &pc,
                 const std::vector<RegVal> &operands) const;
};

} // namespace o3
} // namespace gem5

#endif // __REUSE_BUFFER_HH__
