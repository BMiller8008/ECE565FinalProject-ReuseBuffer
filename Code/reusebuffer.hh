/*
 * reuse_buffer.hh
 *
 * Header file for the ReuseBuffer class used in the gem5 O3 CPU model.
 * The ReuseBuffer uses the instruction address (Addr) and operand values
 * to check for instruction matches and stores the result upon instruction
 * completion, using FIFO replacement.
 */

#ifndef __REUSE_BUFFER_HH__
#define __REUSE_BUFFER_HH__

#include <vector>
#include <deque>
#include "base/statistics.hh"
#include "cpu/o3/comm.hh"
#include "cpu/o3/dyn_inst_ptr.hh"
#include "cpu/o3/inst_queue.hh"
#include "cpu/o3/limits.hh"
#include "cpu/o3/lsq.hh"
#include "cpu/o3/scoreboard.hh"
#include "cpu/timebuf.hh"
#include "debug/IEW.hh"
#include "sim/probe/probe.hh"
#include "cpu/o3/reusebuffer.hh"

#define REUSE_BUFFER_SIZE 1024  // Adjust the size as needed
namespace gem5
{

namespace o3
{

class ReuseBuffer
{
  public:
    // Structure to hold an entry in the reuse buffer
    struct Entry {
    Addr pc;
    std::vector<RegVal> operands;
    std::vector<RegVal> results; // Store up to 2 results
    size_t result_count;

    Entry(Addr _pc, const std::vector<RegVal>& _operands, const std::vector<RegVal>& _results)
        : pc(_pc), operands(_operands), results(_results), result_count(_results.size()) {}
    };


    ReuseBuffer();
    ~ReuseBuffer();

    // Check if an instruction with the same PC and operands exists
    bool contains(Addr pc,
                  const std::vector<RegVal> &operands) const;

    // Get the result of an instruction from the reuse buffer
    std::vector<RegVal> getResults(Addr pc,
                     const std::vector<RegVal> &operands) const;

    // Insert a new instruction into the reuse buffer
    void insert(Addr pc,
                const std::vector<RegVal> &operands,
                const std::vector<RegVal> &result);

  private:
    // The reuse buffer implemented as a deque for FIFO behavior
    std::deque<Entry> buffer;

    // Helper function to compare entries
    bool isMatch(const Entry &entry,
                 Addr pc,
                 const std::vector<RegVal> &operands) const;
};

} // namespace o3
} // namespace gem5

#endif // __REUSE_BUFFER_HH__

