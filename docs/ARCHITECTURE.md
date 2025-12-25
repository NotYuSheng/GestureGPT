# GestureGPT Architecture

## System Overview

GestureGPT is a sign language API that **retrieves pre-recorded ASL videos** from a dataset rather than generating them.

## Architecture Diagram

See [architecture.puml](architecture.puml) for the PlantUML source.

To render the diagram:
```bash
# Using PlantUML CLI
plantuml architecture.puml

# Or online at
# http://www.plantuml.com/plantuml/uml/
```

![Architecture Diagram](architecture.png)

## Component Overview

### 1. API Gateway (FastAPI)
- **OpenAI-compatible endpoints** (`/v1/chat/completions`)
- Request validation and routing
- Response formatting
- Static video file serving

### 2. Text Generation Layer

#### LLM Router
Routes to configured provider based on environment:
- `LLM_PROVIDER=openai` → OpenAI GPT models
- `LLM_PROVIDER=anthropic` → Anthropic Claude
- `LLM_PROVIDER=custom` → Local LLM (Ollama/LM Studio)

#### LLM Providers
- **OpenAI Provider**: GPT-3.5/GPT-4 via OpenAI SDK
- **Anthropic Provider**: Claude models via Anthropic SDK
- **Local LLM Provider**: OpenAI-compatible local models

**Output**: ASL-friendly text (simplified English grammar)

### 3. Sign Language Processing Layer

#### Sign Mapper Service
Converts English text to ASL glosses:

```python
Input:  "Hello! I am feeling good today."
Output: ["HELLO", "I", "FEEL", "GOOD", "TODAY"]

Process:
1. Tokenize text
2. Remove articles (a, an, the)
3. Remove auxiliary verbs (am, is, are)
4. Convert to ASL grammar structure
5. Map to sign glosses
```

#### Video Lookup Service
Retrieves video files from dataset:

```python
Input:  ["HELLO", "FEEL", "GOOD"]
Output: [
    "datasets/wlasl/signs/HELLO.mp4",
    "datasets/wlasl/signs/FEEL.mp4",
    "datasets/wlasl/signs/GOOD.mp4"
]

Fallback Strategy:
1. Exact match in dataset
2. Check synonyms/similar signs
3. Fingerspell if not found
```

#### Video Stitcher
Concatenates videos into final output:

```python
Input:  ["HELLO.mp4", "FEEL.mp4", "GOOD.mp4"]
Output: "cache/response_abc123.mp4"

Process:
1. Load individual sign videos
2. Add smooth transitions (optional)
3. Concatenate using FFmpeg/OpenCV
4. Optimize file size
5. Store in cache
```

#### Cache Service
Two-level caching:

1. **Phrase Cache** (Redis/Memory)
   - Maps text → video URL
   - Fast lookup for common phrases
   - TTL-based expiration

2. **Video Cache** (File System)
   - Stores stitched video files
   - Prevents re-stitching common requests
   - LRU eviction policy

### 4. Storage Layer

#### ASL Video Dataset
Pre-recorded sign language videos:

```
datasets/
├── wlasl/              # WLASL dataset (2,000+ signs)
│   ├── signs/
│   │   ├── HELLO.mp4
│   │   ├── GOOD.mp4
│   │   ├── FEEL.mp4
│   │   └── ...
│   └── metadata.json
├── asl-lex/            # ASL-LEX (2,700+ signs)
│   └── ...
├── fingerspell/        # Fingerspelling alphabet
│   ├── A.mp4
│   ├── B.mp4
│   └── ...
└── phrases/            # Common phrases
    ├── HOW-ARE-YOU.mp4
    ├── THANK-YOU.mp4
    └── ...
```

#### Dataset Index
Metadata mapping for fast lookups:

```json
{
  "HELLO": {
    "path": "datasets/wlasl/signs/HELLO.mp4",
    "duration": 1.2,
    "signer": "signer_01",
    "synonyms": ["HI", "GREETINGS"]
  },
  "FEEL": {
    "path": "datasets/wlasl/signs/FEEL.mp4",
    "duration": 1.5,
    "signer": "signer_02"
  }
}
```

## Data Flow

### Complete Request Flow

```
1. User Request
   POST /v1/chat/completions
   { "messages": [{"role": "user", "content": "Hello!"}] }
   ↓

2. LLM Text Generation
   LLM Router → OpenAI/Claude/Local
   Response: "Hello! I feel good. Thank you ask!"
   ↓

3. Check Phrase Cache
   Key: "Hello! I feel good. Thank you ask!"
   Cache Hit? → Return cached video URL
   Cache Miss? → Continue to step 4
   ↓

4. Sign Mapping
   Input: "Hello! I feel good. Thank you ask!"
   Output: ["HELLO", "I", "FEEL", "GOOD", "THANK", "YOU", "ASK"]
   ↓

5. Video Lookup
   Query Dataset Index
   Results:
   - HELLO → datasets/wlasl/signs/HELLO.mp4
   - I → datasets/wlasl/signs/I.mp4
   - FEEL → datasets/wlasl/signs/FEEL.mp4
   - GOOD → datasets/wlasl/signs/GOOD.mp4
   - THANK-YOU → datasets/phrases/THANK-YOU.mp4
   - ASK → datasets/wlasl/signs/ASK.mp4
   ↓

6. Check Video Cache
   Key: hash(["HELLO", "I", "FEEL", ...])
   Cache Hit? → Return cached stitched video
   Cache Miss? → Continue to step 7
   ↓

7. Video Stitching
   FFmpeg concatenates videos
   Output: cache/response_abc123.mp4
   ↓

8. Update Caches
   - Phrase Cache: "Hello! I feel..." → /videos/response_abc123.mp4
   - Video Cache: Store stitched file
   ↓

9. API Response
   {
     "choices": [{
       "message": {"content": "Hello! I feel good..."},
       "video_url": "http://localhost:8000/videos/response_abc123.mp4"
     }]
   }
```

## Recommended Datasets

### 1. WLASL (Word-Level ASL)
- **Size**: 2,000+ signs
- **Format**: MP4 videos
- **URL**: https://dxli94.github.io/WLASL/
- **License**: Research use

### 2. ASL-LEX
- **Size**: 2,700+ lexical signs
- **Features**: Phonological annotations
- **URL**: https://asllex.org/
- **License**: Academic use

### 3. SignBank
- **Size**: Comprehensive ASL dictionary
- **Quality**: High-quality recordings
- **URL**: http://aslsignbank.haskins.yale.edu/

### 4. Spreadthesign
- **Size**: International sign languages
- **Coverage**: Multiple countries
- **URL**: https://www.spreadthesign.com/

## Implementation Phases

### Phase 1: Sign Mapping (Current Priority)
**Files to create:**
- `app/services/sign_mapper.py`
- `app/services/asl_grammar.py`

**Tasks:**
- Text tokenization
- ASL grammar conversion
- Gloss mapping

### Phase 2: Dataset Integration
**Files to create:**
- `app/services/video_retrieval.py`
- `app/services/dataset_loader.py`

**Tasks:**
- Download WLASL dataset
- Build video index
- Implement lookup service

### Phase 3: Video Stitching
**Files to create:**
- `app/services/video_stitcher.py`
- `app/utils/ffmpeg_wrapper.py`

**Tasks:**
- Video concatenation with FFmpeg
- Smooth transitions
- Performance optimization

### Phase 4: Caching
**Files to create:**
- `app/services/cache_manager.py`

**Tasks:**
- Implement phrase cache (Redis)
- Video file caching
- Cache invalidation strategy

## Performance Considerations

### Video Stitching Optimization
- **Pre-cache common phrases**: "Hello", "Thank you", etc.
- **Lazy loading**: Load datasets on demand
- **Parallel processing**: Stitch multiple videos concurrently
- **Compression**: Optimize video file sizes

### Caching Strategy
```python
# L1: In-memory phrase cache (fast)
phrase_cache = {
  "Hello! How are you?": "/videos/cached_001.mp4"
}

# L2: Video file cache (medium)
video_cache = {
  hash(["HELLO", "HOW", "YOU"]): "cache/video_abc.mp4"
}

# L3: Dataset (slow - requires stitching)
# Only accessed on cache miss
```

### Scaling Considerations
- **CDN**: Serve videos from CDN for faster delivery
- **Compression**: Use H.264 with optimized settings
- **Thumbnails**: Generate preview images
- **Streaming**: Support HLS/DASH for large videos

## Error Handling

### Fallback Strategies

```python
def get_sign_video(gloss: str) -> str:
    # 1. Try exact match
    if gloss in dataset_index:
        return dataset_index[gloss]["path"]

    # 2. Try synonym
    for sign, data in dataset_index.items():
        if gloss in data.get("synonyms", []):
            return data["path"]

    # 3. Fingerspell as last resort
    return fingerspell(gloss)

def fingerspell(word: str) -> List[str]:
    return [f"datasets/fingerspell/{char.upper()}.mp4"
            for char in word if char.isalpha()]
```

## Security Considerations

- **Input validation**: Sanitize text inputs
- **Rate limiting**: Prevent abuse
- **File access**: Restrict to dataset directories
- **CORS**: Configure appropriately
- **Authentication**: Add API keys for production

## Monitoring

**Key Metrics:**
- Cache hit rate (phrase cache)
- Cache hit rate (video cache)
- Average stitching time
- Dataset lookup performance
- API response time
- Storage usage

## Next Steps

1. **Review** this architecture document
2. **Download** WLASL dataset
3. **Implement** sign mapping service
4. **Build** dataset index
5. **Create** video stitching service
6. **Add** caching layer

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for step-by-step implementation instructions.
