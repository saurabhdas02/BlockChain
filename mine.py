from block import Block
import json
from datetime import datetime
import hashlib
import os
import sync


NUM_ZEROES = 5

def generate_header(index, prev_hash, data, timestamp, nonce):
  return str(index) + prev_hash + str(data) + str(timestamp) + str(nonce)

def calculate_hash(index, prev_hash, data, timestamp, nonce):
  header_string = generate_header(index, prev_hash, data, timestamp, nonce)
  sha = hashlib.sha256()
  sha.update(header_string)
  return sha.hexdigest()

def mine(last_block):
  index = int(last_block.index) + 1
  timestamp = datetime.now()
  data = "I block #%s" % (int(last_block.index) + 1)
  prev_hash = last_block.hash
  nonce = 0

  block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
  print(block_hash)
  while str(block_hash[0:NUM_ZEROES]) != '0' * NUM_ZEROES:
    nonce += 1
    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

  #dictionary to create the new block object.
  block_data = {}
  block_data['index'] = index
  block_data['prev_hash'] = last_block.hash
  block_data['timestamp'] = timestamp
  block_data['data'] = "Gimme %s dollars" % index
  block_data['hash'] = block_hash
  block_data['nonce'] = nonce
  return Block(block_data)


if __name__ == '__main__':
  node_blocks = sync.sync()
  # print(node_blocks)
  last_block = node_blocks[-1]
  new_block = mine(last_block)
  new_block.self_save()