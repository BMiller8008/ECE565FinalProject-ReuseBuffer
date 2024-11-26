/*
 * reuse_buffer.cc
 *
 * Implementation of the ReuseBuffer class for the gem5 O3 CPU model.
 */

#include "cpu/o3/reusebuffer.hh"

#include <algorithm> // For std::find_if, std::any_of

namespace gem5
{

namespace o3
{

ReuseBuffer::ReuseBuffer()
{
    // Constructor logic if needed
}

ReuseBuffer::~ReuseBuffer()
{
    // Destructor logic if needed
}

bool
ReuseBuffer::isMatch(const Entry &entry,
                     Addr pc,
                     const std::vector<RegVal> &operands) const
{
    if (entry.pc != pc)
        return false;

    if (entry.operands.size() != operands.size())
        return false;

    for (size_t i = 0; i < operands.size(); ++i) {
        if (entry.operands[i] != operands[i])
            return false;
    }

    return true;
}

bool
ReuseBuffer::contains(Addr pc,
                      const std::vector<RegVal> &operands) const
{
    return std::any_of(buffer.begin(), buffer.end(),
                       [&](const Entry &entry) {
                           return isMatch(entry, pc, operands);
                       });
}

RegVal
ReuseBuffer::getResult(Addr pc,
                       const std::vector<RegVal> &operands) const
{
    auto it = std::find_if(buffer.begin(), buffer.end(),
                           [&](const Entry &entry) {
                               return isMatch(entry, pc, operands);
                           });

    if (it != buffer.end()) {
        return it->result;
    } else {
        // Handle the case where the entry is not found
        // For simplicity, return zero; adjust as needed
        return RegVal(0);
    }
}

void
ReuseBuffer::insert(Addr pc,
                    const std::vector<RegVal> &operands,
                    const RegVal &result)
{
    // Create a new entry
    Entry new_entry(pc, operands, result);

    // Check if the buffer is full
    if (buffer.size() >= REUSE_BUFFER_SIZE) {
        // Remove the oldest entry (FIFO replacement)
        buffer.pop_front();
    }

    // Add the new entry to the buffer
    buffer.push_back(new_entry);
}

} // namespace o3
} // namespace gem5
