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
    DPRINTF(IEW, "OPERANDS EMPTY %d BUFFER EMPYT %d", operands.empty(),buffer.empty());
    if (buffer.empty() || operands.empty()){
        return false;
    }
    return std::any_of(buffer.begin(), buffer.end(),
                       [&](const Entry &entry) {
                           return isMatch(entry, pc, operands);
                       });
}

void
ReuseBuffer::insert(Addr pc,
                    const std::vector<RegVal>& operands,
                    const std::vector<RegVal>& results)
{
    // Create a new entry
    Entry new_entry(pc, operands, results);

    // Check if the buffer is full
    if (!buffer.empty() && buffer.size() >= REUSE_BUFFER_SIZE) {
        buffer.pop_front(); // Remove the oldest entry
    }

    // Add the new entry to the buffer
    buffer.push_back(new_entry);
}

std::vector<RegVal>
ReuseBuffer::getResults(Addr pc,
                        const std::vector<RegVal>& operands) const
{
    auto it = std::find_if(buffer.begin(), buffer.end(),
                           [&](const Entry& entry) {
                               return isMatch(entry, pc, operands);
                           });

    DPRINTF(IEW, "after it %d\n", it != buffer.end());
    DPRINTF(IEW, "it->result_count %d\n",it->result_count);

    if (it != buffer.end()) {
        Entry matchedEntry = *it;
        std::vector<RegVal> regResults;
        DPRINTF(IEW, "matched entry size %d\n",matchedEntry.result_count);
        DPRINTF(IEW, "it->results empty? %d\n",matchedEntry.results.empty());
        DPRINTF(IEW, "regresults1 %lu\n", it->results[0]);
        for (int i = 0; i < it->result_count; ++i) {
            DPRINTF(IEW, "GET HERE???????\n");
            DPRINTF(IEW, "regresults[%d] = %lu\n", i, it->results[i]);
            regResults.push_back(it->results[i]);
        }
        // s = std::vector<RegVal>(it->results.begin(), it->results.begin() + it->result_count);
        return regResults;

    } else {
        return {}; // Empty vector if not found
    }
}

} // namespace o3
} // namespace gem5


