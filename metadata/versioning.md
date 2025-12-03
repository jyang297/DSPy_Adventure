# DSPy Course Versioning

## Version Management

### Current Version
- **Course Version**: 1.0.0
- **Target DSPy Version**: 2.5+
- **Last Updated**: 2025-12-03
- **Status**: Initial Release

---

## Versioning Philosophy

### Course Versioning (Semantic)
We use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes in course structure or learning approach
- **MINOR**: New modules, significant pattern updates, DSPy API changes
- **PATCH**: Bug fixes, typo corrections, minor clarifications

### DSPy Compatibility
Each course version targets a range of DSPy versions:
- **Current Target**: DSPy 2.5+
- **Tested With**: 2.5.0, 2.5.1, 2.5.2
- **Minimum**: 2.5.0
- **Expected Compatible**: 2.x series

---

## Version History

### v1.0.0 (2025-12-03)
**Initial Release**

**Content**:
- 10 complete modules (Signatures through Best Practices)
- 3 project reproduction guides
- Complete metadata and reference documentation
- Template system for future modules

**DSPy Features Covered**:
- Core APIs: Signatures, Modules, Predict, ChainOfThought, ReAct
- Optimizers: MIPROv2, BootstrapRS, GEPA, BootstrapFinetune
- Advanced: RAG, Agents, Evaluation

**Referenced Projects**:
- gabrielvanderlei/DSPy-examples
- Scale3-Labs/dspy-examples
- diicellman/dspy-gradio-rag
- Weaviate recipes
- Isaac Kargar's multi-agent article

---

## DSPy Version Tracking

### DSPy 2.5+ (Target)
**Release Date**: Late 2024 / Early 2025
**Key Features**:
- Mature optimizer APIs
- Stable Signature/Module system
- Production-ready components

**Course Alignment**: Full compatibility

### DSPy 2.0-2.4
**Compatibility**: Likely compatible with minor adjustments
**Known Issues**:
- Some optimizer names may differ
- API signatures may vary slightly

**Migration Notes**: Check DSPy release notes

### DSPy 1.x (Legacy)
**Compatibility**: Not guaranteed
**Known Issues**:
- Teleprompter terminology (deprecated in 2.x)
- Different optimizer APIs
- Module structure changes

**Migration Notes**: Upgrade to 2.5+ recommended

---

## Breaking Changes Policy

### When We'll Bump MAJOR Version

1. **Course Restructure**
   - Change in module order or hierarchy
   - Significant pedagogy shifts
   - Removal of entire modules

2. **DSPy API Breaks**
   - DSPy 3.0+ with incompatible APIs
   - Removal of core features we rely on

3. **Project Reference Changes**
   - All referenced projects deprecated
   - Complete pattern overhaul

### When We'll Bump MINOR Version

1. **New Content**
   - Additional modules
   - New project reproductions
   - Significant pattern additions

2. **DSPy Updates**
   - New optimizer coverage
   - API improvements
   - New official features

3. **Pattern Updates**
   - Community best practices evolve
   - Better production patterns discovered

### When We'll Bump PATCH Version

1. **Fixes**
   - Code bugs
   - Typos
   - Broken links

2. **Clarifications**
   - Better explanations
   - Additional comments
   - Improved examples (non-breaking)

---

## Module-Specific Versions

Each module tracks its own metadata:

```json
{
  "module": "01-signatures",
  "version": "1.0.0",
  "dspy_version": "2.5+",
  "last_updated": "2025-12-03",
  "status": "stable"
}
```

### Module Statuses
- **stable**: Production-ready, well-tested
- **beta**: Complete but may have minor issues
- **experimental**: New content, feedback needed
- **deprecated**: Superseded by newer module

---

## Compatibility Matrix

| Course Version | DSPy Version | Python | Status |
|----------------|--------------|--------|--------|
| 1.0.0 | 2.5+ | 3.9+ | Current |
| 1.0.0 | 2.0-2.4 | 3.9+ | Likely Compatible |
| 1.0.0 | 1.x | 3.8+ | Not Compatible |

### Dependency Versions

**Core Dependencies**:
- `dspy-ai>=2.5.0`
- `python>=3.9`

**Optional Dependencies** (by module):
- `openai>=1.0.0` (for OpenAI LMs)
- `anthropic>=0.18.0` (for Claude LMs)
- `weaviate-client>=3.0.0` (Module 06)
- `gradio>=4.0.0` (Project A)
- `fastapi>=0.109.0` (Project A)

---

## Update Strategy

### How We Track DSPy Changes

1. **Monitor Official Repo**
   - Watch stanfordnlp/dspy releases
   - Track breaking changes in release notes

2. **Test Regularly**
   - Run all module examples against new DSPy versions
   - Update compatibility matrix

3. **Community Feedback**
   - GitHub issues for compatibility problems
   - User reports of API changes

### Update Frequency

- **PATCH**: As needed (bug fixes)
- **MINOR**: Quarterly (new content, pattern updates)
- **MAJOR**: Yearly or on DSPy breaking changes

---

## Migration Guides

### Upgrading Course Version

#### From Future 1.x to 2.0 (When Available)
- TBD based on actual breaking changes

### Upgrading DSPy Version

#### From DSPy 2.4 to 2.5+
No course changes needed. Examples should work with both.

**Potential Issues**:
- Check optimizer initialization parameters
- Verify metric function signatures

**Testing**:
```bash
# Test all modules
cd dspy-course/
python scripts/test_all_modules.py
```

---

## Deprecation Policy

### How We Deprecate Content

1. **Announcement** (one MINOR version ahead)
   - Mark module/pattern as deprecated
   - Provide migration path
   - Update documentation

2. **Deprecation** (current version)
   - Module still available
   - Clear warnings in code
   - Alternative recommended

3. **Removal** (next MAJOR version)
   - Deprecated content removed
   - Migration guide available
   - Archive in `legacy/` directory

### Currently Deprecated
- None (initial release)

### Planned Deprecations
- None currently planned

---

## Contributing to Versioning

### Version Bump Criteria

**Suggest PATCH** when fixing:
- Typos in documentation
- Code bugs that don't change API
- Broken example code
- Dead links

**Suggest MINOR** when adding:
- New examples in existing modules
- New sub-sections
- Better explanations
- New project references

**Suggest MAJOR** when:
- Restructuring entire course
- Removing modules
- Changing fundamental approach

### Pull Request Guidelines

Include in PR description:
- Proposed version bump (PATCH/MINOR/MAJOR)
- Reason for change
- Affected modules
- DSPy version compatibility impact

---

## Version Manifest

### File Locations

Version information stored in:
- `/metadata/versioning.md` (this file)
- `/VERSION` (root file with current version)
- `/modules/*/meta/difficulty.json` (per-module versions)
- `/CHANGELOG.md` (detailed changes)

### Version Check

```bash
# Check course version
cat VERSION

# Check DSPy compatibility
python -c "import dspy; print(dspy.__version__)"

# Verify compatibility
python scripts/check_compatibility.py
```

---

## Changelog

Detailed changes tracked in `/CHANGELOG.md`

### Format
```markdown
## [1.0.0] - 2025-12-03
### Added
- Initial release with 10 modules
- Project reproduction guides
- Complete documentation

### Changed
- N/A (initial release)

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
```

---

## Future Roadmap

### Planned for v1.1.0 (Q2 2025)
- Module 11: Multi-Modal DSPy
- Additional RAG patterns
- More production deployment examples

### Planned for v1.2.0 (Q3 2025)
- Module 12: DSPy at Scale
- Distributed optimization
- Cost optimization deep-dive

### Planned for v2.0.0 (When DSPy 3.0 Releases)
- Full compatibility with DSPy 3.0+
- Restructure based on new APIs
- Expanded agent patterns

---

## Version Support

### Support Timeline

- **Current Version**: Full support (bug fixes, updates)
- **Previous MINOR**: Security fixes only (6 months)
- **Older Versions**: Community support via issues

### End of Life

Versions marked EOL:
- None yet (initial release)

---

## Questions & Feedback

### Version-Related Issues

**Report**:
- Compatibility problems: Tag with `compatibility`
- Version confusion: Tag with `documentation`
- Deprecation concerns: Tag with `deprecation`

**Where**:
- GitHub Issues: This repository
- Discussions: For clarifications

---

**Version Management Last Updated**: 2025-12-03
**Next Review Date**: 2025-03-03
