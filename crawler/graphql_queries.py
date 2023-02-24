QUERY_SOLUTIONS = '''
query questionSolutionVideoArticles($questionSlug: String!, $orderBy: SolutionArticleOrderBy, $userInput: String, $tagSlugs: [String!], $skip: Int, $first: Int) {
  questionSolutionVideoArticles(questionSlug: $questionSlug, orderBy: $orderBy, userInput: $userInput, tagSlugs: $tagSlugs, skip: $skip, first: $first) {
    totalNum
    edges {
      node {
        title
        slug
        chargeType
        isEditorsPick
        byLeetcode
        videosInfo {
          videoId
          coverUrl
          duration
          __typename
        }
        hitCount
        __typename
      }
      __typename
    }
    __typename
  }
}
'''

QUERY_SOLUTION = '''
query solutionDetailArticle($slug: String!, $orderBy: SolutionArticleOrderBy!) {
  solutionArticle(slug: $slug, orderBy: $orderBy) {
    ...solutionArticle
    content
    question {
      questionTitleSlug
      __typename
    }
    position
    next {
      slug
      title
      __typename
    }
    prev {
      slug
      title
      __typename
    }
    __typename
  }
}

fragment solutionArticle on SolutionArticleNode {
  ipRegion
  rewardEnabled
  canEditReward
  uuid
  title
  slug
  sunk
  chargeType
  status
  identifier
  canEdit
  canSee
  reactionType
  reactionsV2 {
    count
    reactionType
    __typename
  }
  tags {
    name
    nameTranslated
    slug
    tagType
    __typename
  }
  createdAt
  thumbnail
  author {
    username
    profile {
      userAvatar
      userSlug
      realName
      __typename
    }
    __typename
  }
  summary
  topic {
    id
    commentCount
    viewCount
    __typename
  }
  byLeetcode
  isMyFavorite
  isMostPopular
  isEditorsPick
  hitCount
  videosInfo {
    videoId
    coverUrl
    duration
    __typename
  }
  __typename
}
'''
